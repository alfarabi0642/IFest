# main.py
import os
import io
import uuid
import logging
import asyncio
import json
import gridfs
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
from bson import ObjectId
from fastapi.responses import StreamingResponse, FileResponse

from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
# removed motor import (we use pymongo via database.py)
from PIL import Image
import requests

# Import your existing blocking pymongo collections
# make sure database.py is in the same folder or in PYTHONPATH
from database import contracts_collection as docs_col

# Optional libs - may not be installed in all environments
try:
    import pytesseract
except Exception:
    pytesseract = None

# Attempt to use PyMuPDF (fitz) to extract native PDF text if available
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

load_dotenv()

# Config (read from env or defaults)
# Note: prefer configuring MONGO_URI in .env in database.py rather than hardcoding here.
OCR_SERVICE_URL = os.getenv("OCR_SERVICE_URL", "").strip() or None
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip() or None
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/ilcsense_uploads")
MAX_FILE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "15"))
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

os.makedirs(UPLOAD_DIR, exist_ok=True)
FALLBACK_DB_DIR = os.path.join(UPLOAD_DIR, "fallback_db")
os.makedirs(FALLBACK_DB_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ilcsense")

app = FastAPI(title="ILCSense Backend (Upload + OCR + Summarize)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for upload response
class UploadOut(BaseModel):
    doc_id: str
    filename: str
    status: str
    message: Optional[str] = None

# ------------ Helpers ------------

def save_bytes_to_file(b: bytes, path: str):
    with open(path, "wb") as f:
        f.write(b)
    return path

async def save_upload_file_tmp(upload_file: UploadFile, dest_path: str) -> str:
    contents = await upload_file.read()
    save_bytes_to_file(contents, dest_path)
    return dest_path

def extract_text_with_pymupdf(path: str) -> str:
    # Return native PDF text if file is PDF and fitz installed
    try:
        if not fitz:
            return ""
        doc = fitz.open(path)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text("text"))
        return "\n".join(text_parts).strip()
    except Exception:
        logger.exception("PyMuPDF extraction failed")
        return ""

def ocr_with_pytesseract_from_image(path: str) -> str:
    if not pytesseract:
        logger.warning("pytesseract not installed")
        return ""
    try:
        img = Image.open(path)
        return pytesseract.image_to_string(img)
    except Exception:
        logger.exception("pytesseract image OCR failed")
        return ""

def call_external_ocr_service(path: str) -> str:
    if not OCR_SERVICE_URL:
        return ""
    try:
        with open(path, "rb") as f:
            files = {"file": (os.path.basename(path), f, "application/octet-stream")}
            resp = requests.post(OCR_SERVICE_URL, files=files, timeout=60)
            resp.raise_for_status()
            j = resp.json()
            return j.get("text", "")
    except Exception:
        logger.exception("OCR service call failed")
        return ""

def summarize_text_local(text: str) -> str:
    # cheap deterministic fallback: first 3 non-empty lines as bullets
    if not text:
        return "No text extracted."
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    bullets = lines[:3] if lines else [text[:200]]
    return "\n".join(f"- {b}" for b in bullets)

def summarize_with_openai(text: str) -> str:
    # Minimal OpenAI Chat completion call via REST — you can replace with SDK.
    if not OPENAI_API_KEY:
        return summarize_text_local(text)
    try:
        prompt = f"Summarize this contract into 3 short bullet points:\n\n{text[:4000]}"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role":"user","content":prompt}],
            "temperature": 0,
            "max_tokens": 300
        }
        r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        j = r.json()
        return j["choices"][0]["message"]["content"].strip()
    except Exception:
        logger.exception("OpenAI summarization failed")
        return summarize_text_local(text)

def detect_quick_flags(text: str):
    flags = []
    low = (text or "").lower()
    if "auto-renew" in low or "automatic renewal" in low or "auto renew" in low:
        flags.append({"clause":"auto_renew","severity":"medium","excerpt":"contains auto-renew wording"})
    if "penalty" in low or "liquidated damages" in low:
        flags.append({"clause":"penalty","severity":"high","excerpt":"contains penalty wording"})
    if "termination for convenience" in low or "terminate" in low:
        flags.append({"clause":"termination","severity":"medium","excerpt":"contains termination wording"})
    return flags

def save_doc_record_fallback(doc_record: dict):
    """Simpan metadata dokumen ke file lokal sebagai fallback jika DB down."""
    fname = f"{doc_record['doc_id']}.json"
    path = os.path.join(FALLBACK_DB_DIR, fname)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc_record, f, default=str, ensure_ascii=False, indent=2)
        logger.warning("Saved doc_record fallback to %s", path)
    except Exception:
        logger.exception("Failed to save fallback doc_record")

async def save_file_to_gridfs(contents: bytes, filename: str, content_type: Optional[str] = None) -> str:
    """
    Save bytes into GridFS and return the inserted file id as string.
    Runs gridfs put in a thread (pymongo/gridfs is blocking).
    """
    def _put():
        fs = gridfs.GridFS(docs_col.database)
        metadata = {}
        if content_type:
            metadata["contentType"] = content_type
        file_id = fs.put(contents, filename=filename, **({"contentType": content_type} if content_type else {}))
        return str(file_id)
    return await asyncio.to_thread(_put)

async def get_file_from_gridfs(file_id: str):
    """
    Return dict {data: bytes, filename: str, content_type: Optional[str]} by reading GridFS entry.
    """
    def _get():
        fs = gridfs.GridFS(docs_col.database)
        grid_out = fs.get(ObjectId(file_id))
        data = grid_out.read()
        # gridfs stores metadata fields case-sensitively; contentType often used
        content_type = getattr(grid_out, "contentType", None) or grid_out._file.get("contentType") or None
        return {"data": data, "filename": grid_out.filename, "content_type": content_type}
    return await asyncio.to_thread(_get)

# ------------ Async DB wrappers (pymongo blocking -> run in thread) ------------

async def db_insert_one(collection, document: dict):
    try:
        result = await asyncio.to_thread(collection.insert_one, document)
        return getattr(result, "inserted_id", None)
    except Exception:
        logger.exception("db_insert_one failed")
        raise

async def db_update_one(collection, filter_q: dict, update: dict):
    try:
        result = await asyncio.to_thread(collection.update_one, filter_q, update)
        return result.raw_result if result else None
    except Exception:
        logger.exception("db_update_one failed")
        raise

async def db_find_one(collection, filter_q: dict):
    try:
        doc = await asyncio.to_thread(collection.find_one, filter_q, {"_id": 0})
        return doc
    except Exception:
        logger.exception("db_find_one failed")
        raise

async def db_find_all(collection, projection: dict = None) -> List[dict]:
    try:
        # run blocking find and build list in a thread
        def _list_all():
            proj = projection if projection is not None else {"_id": 0}
            cursor = collection.find({}, proj)
            return [d for d in cursor]
        return await asyncio.to_thread(_list_all)
    except Exception:
        logger.exception("db_find_all failed")
        raise

# ------------ Background job ------------

async def process_document_job(doc_id: str, file_path: str):
    logger.info("Start processing %s", doc_id)
    # 1. Attempt native PDF extraction first
    text = extract_text_with_pymupdf(file_path)
    # 2. If no native text, try external OCR service
    if not text and OCR_SERVICE_URL:
        text = call_external_ocr_service(file_path)
    # 3. If still empty and pytesseract is available, try local image OCR
    if not text and pytesseract:
        # Note: this will work if the file is an image; for multi-page PDFs it's limited.
        text = ocr_with_pytesseract_from_image(file_path)
    # Ensure text is a string
    text = text or ""
    # 4. Summarize (OpenAI if available else fallback)
    summary = summarize_with_openai(text) if OPENAI_API_KEY else summarize_text_local(text)
    # 5. Quick rule-based flags
    flags = detect_quick_flags(text)
    # 6. Update DB (wrapped)
    update = {
        "status": "processed",
        "text": text,
        "summary": summary,
        "flags": flags,
        "processed_at": datetime.utcnow()
    }
    try:
        await db_update_one(docs_col, {"doc_id": doc_id}, {"$set": update})
    except Exception:
        # if DB update fails, write fallback and log
        logger.exception("Failed to update document in DB, writing fallback metadata")
        save_doc_record_fallback({"doc_id": doc_id, **update})
    logger.info("Finished processing %s", doc_id)

# ------------ Endpoints ------------

@app.post("/upload", response_model=UploadOut, status_code=201)
async def upload_endpoint(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # check size
    contents = await file.read()
    if len(contents) > MAX_FILE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_FILE_MB} MB.")
    # create doc_id and save file to disk (local backup)
    doc_id = "doc_" + uuid.uuid4().hex
    filename = f"{doc_id}__{file.filename}"
    dest_path = os.path.join(UPLOAD_DIR, filename)
    save_bytes_to_file(contents, dest_path)

    # Save file to GridFS (best-effort). If GridFS fails, we continue but metadata will note it.
    gridfs_id = None
    try:
        gridfs_id = await save_file_to_gridfs(contents, filename=file.filename, content_type=file.content_type)
        logger.info("Saved file to GridFS with id %s", gridfs_id)
    except Exception:
        logger.exception("Failed to save file to GridFS; continuing with local storage only")

    # create DB record (include reference to GridFS if available)
    doc_record = {
        "doc_id": doc_id,
        "filename": file.filename,
        "storage": {
            "type": "disk",
            "path": dest_path,
            "gridfs_id": gridfs_id  # may be None if gridfs failed
        },
        "uploaded_at": datetime.utcnow(),
        "status": "uploaded"
    }

    # try insert into Mongo (in thread). fallback to local file if fails.
    try:
        await db_insert_one(docs_col, doc_record)
    except Exception:
        logger.exception("Mongo insert failed, using fallback")
        save_doc_record_fallback(doc_record)

    # schedule background processing safely by creating an asyncio task
    try:
        asyncio.create_task(process_document_job(doc_id, dest_path))
    except RuntimeError:
        background_tasks.add_task(lambda d, p: asyncio.create_task(process_document_job(d, p)), doc_id, dest_path)

    return UploadOut(doc_id=doc_id, filename=file.filename, status="uploaded", message="processing started")

@app.get("/doc/{doc_id}")
async def get_document(doc_id: str):
    try:
        doc = await db_find_one(docs_col, {"doc_id": doc_id})
    except Exception:
        # attempt fallback file read
        fallback_path = os.path.join(FALLBACK_DB_DIR, f"{doc_id}.json")
        if os.path.exists(fallback_path):
            with open(fallback_path, "r", encoding="utf-8") as f:
                doc = json.load(f)
        else:
            raise HTTPException(status_code=500, detail="internal error reading document")
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    return JSONResponse(doc)

@app.get("/docs")
async def list_docs():
    try:
        lst = await db_find_all(docs_col, {"_id": 0, "text": 0})
    except Exception:
        # fallback: list fallback files
        lst = []
        for p in Path(FALLBACK_DB_DIR).glob("*.json"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data.pop("text", None)
                    lst.append(data)
            except Exception:
                continue
    return lst

@app.post("/process/{doc_id}")
async def reprocess(doc_id: str, background_tasks: BackgroundTasks):
    try:
        doc = await db_find_one(docs_col, {"doc_id": doc_id})
    except Exception:
        doc = None
    if not doc:
        # try fallback file
        fallback_path = os.path.join(FALLBACK_DB_DIR, f"{doc_id}.json")
        if os.path.exists(fallback_path):
            with open(fallback_path, "r", encoding="utf-8") as f:
                doc = json.load(f)
        else:
            raise HTTPException(status_code=404, detail="not found")

    path = doc.get("storage", {}).get("path")
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="uploaded file not found")

    # update status in DB (best-effort)
    try:
        await db_update_one(docs_col, {"doc_id": doc_id}, {"$set": {"status": "processing"}})
    except Exception:
        logger.exception("Failed to set status to processing in DB; continuing")

    try:
        asyncio.create_task(process_document_job(doc_id, path))
    except RuntimeError:
        background_tasks.add_task(lambda d, p: asyncio.create_task(process_document_job(d, p)), doc_id, path)

    return {"doc_id": doc_id, "status": "processing"}

@app.get("/download/{doc_id}")
async def download_document(doc_id: str):
    # fetch metadata
    try:
        doc = await db_find_one(docs_col, {"doc_id": doc_id})
    except Exception:
        doc = None

    if not doc:
        # try fallback metadata file
        fallback_path = os.path.join(FALLBACK_DB_DIR, f"{doc_id}.json")
        if os.path.exists(fallback_path):
            with open(fallback_path, "r", encoding="utf-8") as f:
                doc = json.load(f)
        else:
            raise HTTPException(status_code=404, detail="document not found")

    storage = doc.get("storage", {})
    gridfs_id = storage.get("gridfs_id")
    if not gridfs_id:
        # fallback: file saved on disk — stream it directly
        file_path = storage.get("path")
        if file_path and os.path.exists(file_path):
            return FileResponse(path=file_path, filename=doc.get("filename"), media_type="application/pdf")
        else:
            raise HTTPException(status_code=404, detail="file not found on disk or gridfs")

    # If gridfs_id present, fetch bytes from GridFS
    try:
        res = await get_file_from_gridfs(gridfs_id)
    except Exception:
        logger.exception("Failed to read file from GridFS")
        raise HTTPException(status_code=500, detail="failed to read file from storage")

    data = res["data"]
    fname = res["filename"] or doc.get("filename") or "download"
    mtype = res["content_type"] or "application/octet-stream"
    return StreamingResponse(io.BytesIO(data), media_type=mtype, headers={"Content-Disposition": f'attachment; filename="{fname}"'})


@app.get("/health")
async def health():
    return {"status": "ok"}
