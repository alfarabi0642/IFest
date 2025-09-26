import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from database import db
from services import ocr_service, analysis_service, embedding_service

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Contract Management API",
    description="API for processing and querying legal contracts.",
    version="1.0.0"
)
# --- 2. ADD THE CORS MIDDLEWARE CONFIGURATION ---

# List of origins that are allowed to make requests to this API.
# The default port for Vite React apps is 5173. 3000 is for Create React App.
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)
# --- Pydantic Models for Request/Response Bodies ---
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    source_chunks: list[str]

# --- Helper function for the background task ---
def process_contract_flow(temp_pdf_path: str, original_filename: str):
    """The full OCR -> Analysis -> Embedding pipeline."""
    print(f"Starting background processing for {original_filename}")
    try:
        # 1. OCR PDF to Text
        contract_name = os.path.splitext(original_filename)[0]
        cleaned_text_path = ocr_service.process_pdf_to_text(temp_pdf_path)
        
        with open(cleaned_text_path, 'r', encoding='utf-8') as f:
            contract_text = f.read()

        # 2. Analyze Text, Generate Embeddings, and Save to DB
        if contract_text:
            analysis_service.analyze_contract_text(contract_text, contract_name)
        else:
            print(f"Warning: No text extracted from {original_filename}")

    except Exception as e:
        print(f"An error occurred during background processing: {e}")
    finally:
        # 3. Clean up temporary files
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        if 'cleaned_text_path' in locals() and os.path.exists(cleaned_text_path):
            os.remove(cleaned_text_path)
        print(f"Finished background processing for {original_filename}")


# --- API Endpoints ---

@app.post("/contracts/upload", status_code=202)
async def upload_contract(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Uploads a PDF contract. The file is processed in the background.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
        
    # Save the uploaded file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_pdf_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Add the long-running job to the background
    background_tasks.add_task(process_contract_flow, temp_pdf_path, file.filename)

    return {"message": "File uploaded successfully. Processing has started in the background."}

# In your main.py file

# In your main.py file

@app.get("/contracts")
async def get_all_contracts():
    """
    Retrieves a list of all processed contracts with enhanced summary data.
    """
    # We now project the entire contractSummarization object to get all needed fields
    projection = {
        "_id": 1,
        "created_at": 1,
        "analysis.contractMetadata": 1,
        "analysis.contractSummarization": 1, # <-- This gets all the new fields
    }
    contracts = list(db.contracts.find({}, projection))
    
    # Process the results for the frontend
    for contract in contracts:
        contract["documentId"] = contract.pop("_id")
        if 'created_at' in contract:
            contract['created_at'] = contract['created_at'].isoformat()
    return contracts

@app.get("/contracts/{document_id}")
async def get_contract_details(document_id: str):
    """
    Retrieves the full analysis details for a specific contract by its ID.
    """
    # Find the document by its string ID
    contract_data = db.contracts.find_one({"_id": document_id})
    
    if contract_data:
        # The 'analysis' field contains all the JSON data we need
        analysis_details = contract_data.get("analysis")
        if analysis_details:
            return analysis_details
        else:
            # Handle case where the document exists but has no analysis field
            raise HTTPException(status_code=404, detail="Analysis details not found for this contract.")
    
    # Handle case where no contract with that ID was found
    raise HTTPException(status_code=404, detail=f"Contract with ID '{document_id}' not found.")

# ... (other code) ...

@app.post("/contracts/{document_id}/query", response_model=QueryResponse)
async def query_contract(document_id: str, request: QueryRequest):
    """
    Asks a question about a specific contract using vector search (RAG).
    """
    # 1. Get the embedding for the user's query
    query_vector = embedding_service.get_embedding(request.query)
    
    # 2. Perform vector search on the NEW 'contract_chunks' collection
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index", # The name of your new vector index
                "path": "embedding_vector", # The simplified path
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 5,
                "filter": {"contract_id": document_id} # Filter to search only in the specified contract
            }
        },
        {
            "$project": {
                "_id": 0,
                "text_content": 1, # Project the text content directly
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    # Run the aggregation on the correct collection
    results = list(db.contract_chunks.aggregate(pipeline))
    
    if not results:
        return QueryResponse(answer="I couldn't find any relevant information in the contract to answer your question.", source_chunks=[])

    # 3. Build the context (now much simpler)
    source_chunks = [result['text_content'] for result in results]
    context = "\n---\n".join(source_chunks)
    
    # 4. Ask the chat model to answer based on the context
    prompt = f"""
    Based *only* on the following context from a legal document, answer the user's question.
    If the answer is not in the context, say so.
    
    Context:
    {context}
    
    Question: {request.query}
    """
    
    chat_client = analysis_service.client
    resp = chat_client.chat.completions.create(
        model=analysis_service.DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = resp.choices[0].message.content
    
    return QueryResponse(answer=answer, source_chunks=source_chunks)