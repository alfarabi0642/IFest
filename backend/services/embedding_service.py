import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import AzureOpenAI
from database import db

# --- Initialize Azure Client ---
client = AzureOpenAI(
    api_key=os.getenv("AZURE_EMBEDDING_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT")
)
DEPLOYMENT_NAME = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")

def get_embedding(text: str) -> list[float]:
    """Generates an embedding for a given text string."""
    response = client.embeddings.create(input=text, model=DEPLOYMENT_NAME)
    return response.data[0].embedding

def create_and_store_embeddings(document_id: str, contract_name: str, full_document_text: str):
    """Splits a document into chunks, generates embeddings, and stores them in MongoDB."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunks = text_splitter.split_text(full_document_text)
    
    print(f"--- Document split into {len(chunks)} chunks. ---")
    
    chunk_list_for_db = []
    for i, chunk_text in enumerate(chunks):
        print(f"  - Processing chunk {i+1} of {len(chunks)}")
        vector = get_embedding(chunk_text)
        chunk_data = {
            "text_content": chunk_text,
            "embedding_vector": vector
        }
        chunk_list_for_db.append(chunk_data)

    final_embedding_data = {
        "contract_id": document_id,
        "contract_name": contract_name,
        "chunks": chunk_list_for_db
    }
    
    db.embedding_vector.insert_one(final_embedding_data)
    print(f"--- Stored embeddings for {document_id} in the database. ---")

# ... (imports and other functions remain the same) ...

def create_and_store_embeddings(document_id: str, contract_name: str, full_document_text: str):
    """
    Splits a document into chunks, generates embeddings, and stores EACH CHUNK
    as a separate document in MongoDB.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    chunks = text_splitter.split_text(full_document_text)
    
    print(f"--- Document split into {len(chunks)} chunks. ---")
    
    documents_to_insert = []
    for i, chunk_text in enumerate(chunks):
        print(f"  - Processing chunk {i+1} of {len(chunks)}")
        vector = get_embedding(chunk_text)
        
        # Create a separate document for each chunk
        chunk_document = {
            "contract_id": document_id,
            "contract_name": contract_name,
            "chunk_index": i, # Optional, but good for ordering
            "text_content": chunk_text,
            "embedding_vector": vector
        }
        documents_to_insert.append(chunk_document)

    # Use insert_many for efficiency
    if documents_to_insert:
        # We will store these in a new, dedicated collection
        db.contract_chunks.insert_many(documents_to_insert)
        print(f"--- Stored {len(documents_to_insert)} embedding chunks for {document_id} in the 'contract_chunks' collection. ---")
    
    # You can now delete the old 'embedding_vector' collection if you want
    # db.embedding_vector.drop()