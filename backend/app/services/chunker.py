import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import AzureOpenAI

deployment = "text-embedding-3-large"
client = AzureOpenAI(
    api_key="47bYCKK9oQRkv9c9o6SaOHvKlRF3g0bqM1CO1DrWthtjVYpymjksJQQJ99BIACHYHv6XJ3w3AAAAACOGVQy1",
    api_version="2023-05-15",
    azure_endpoint="https://embbedder-resource.cognitiveservices.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
)
    
# --- 1. Your Initial Data ---
OUTPUT_DIR = "output"
JSON_OUTPUT_DIR = "json"
full_document_text = ""

txt_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".txt")]
for file in txt_files:
    doc_name = os.path.splitext(file)[0]
    file_path = os.path.join(OUTPUT_DIR, file)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        full_document_text += f.read() + "\n"
        
# --- 2. Placeholder for the Real Embedding Function ---

def get_embedding(text: str) -> list[float]:

    response = client.embeddings.create(
        input=text,
        model=deployment
    )
    
    return response.data[0].embedding


# --- 3. The Processing Logic ---

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # A smaller size for this example text
    chunk_overlap=50
)

# Split the document into text chunks
print(f"--- Splitting document '{doc_name}' into chunks... ---")
chunks = text_splitter.split_text(full_document_text)
print(f"--- Document split into {len(chunks)} chunks. ---")

# This is the list where we will store the dictionaries for each chunk
chunk_list_for_json = []

print("\n--- Processing each chunk to get its embedding... ---")
# Loop through the text chunks
for i, chunk_text in enumerate(chunks):
    print(f"  - Processing chunk {i+1} of {len(chunks)}")
    
    # Get the embedding vector for the current chunk
    vector = get_embedding(chunk_text)
    
    # Create a dictionary for this single chunk
    chunk_data = {
        "text_content": chunk_text,
        "embedding_vector": vector
    }
    
    # Add this chunk's dictionary to our main list
    chunk_list_for_json.append(chunk_data)

print("--- Finished processing all chunks. ---\n")

# --- 4. Assemble the Final JSON Structure ---

print("--- Assembling the final JSON object... ---")
# Create the final, top-level dictionary that matches your desired format
final_json_data = {
    "doc_name": doc_name,
    "chunks": chunk_list_for_json
}

# --- 5. Final Output and Saving ---

# Pretty-print the final JSON to the console to verify it's correct
print("\n--- Final JSON Output ---")
print(json.dumps(final_json_data, indent=2))

# Now you can save this single object to a database or file
# Example: Saving to a JSON file
output_filename = f"{doc_name}.json"
json_path = os.path.join(JSON_OUTPUT_DIR, output_filename)
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(final_json_data, f, ensure_ascii=False, indent=2)

print("Saved JSON:", json_path)

"""
# cleanup temp folders
shutil.rmtree(JSON_OUTPUT_PATH, ignore_errors=True)
print("Deleted temp folder:", JSON_OUTPUT_PATH)

shutil.rmtree(OUTPUT_PATH, ignore_errors=True)
print("Deleted temp folder:", OUTPUT_PATH)

shutil.rmtree(pdfs, ignore_errors=True)
print("Deleted temp folder:", pdfs)
"""
