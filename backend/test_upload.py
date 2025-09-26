from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    """
    A minimal endpoint to test file uploads.
    It just receives a file and returns its details.
    """
    if not file:
        return {"error": "No file sent"}
    else:
        return {
            "filename": file.filename,
            "content_type": file.content_type
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)