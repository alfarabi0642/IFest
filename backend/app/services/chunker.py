import json
import numpy as np  # Used to create realistic fake embedding vectors
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- 1. Your Initial Data ---

document_id = "CTR-MSA-2024-00123"

# A more realistic multi-paragraph text for better chunking demonstration
full_document_text = """
Jakarta - Sebanyak 4.645 personel gabungan Polri, TNI, dan pemda DKI diterjunkan hari ini untuk melakukan pengamanan unjuk rasa di sejumlah titik. Sejauh ini, akan ada tiga unjuk rasa dari berbagai elemen masyarakat di wilayah Jakarta Pusat (Jakpus).
"Kuat pengamanan wilayah Jakpus 4.645 personel gabungan Polri, TNI, dan pemda DKI," kata Kapolres Metro Jakarta Pusat Kombes Susatyo Purnomo Condro kepada wartawan, Kamis (25/9/2025).
Dia mengatakan demonstrasi hari ini terbagi di tiga titik, yakni di Silang Selatan Monas, Kementerian Lingkungan Hidup (LH), serta Jalan Jenderal Sudirman.
Dia menjelaskan di Silang Selatan Monas dan Kementerian LH, unjuk rasa dilakukan oleh Koalisi Nasional Untuk Reforma Agraria. Sementara itu, aksi di Jalan Sudirman dilakukan oleh Asosiasi Petani Sawit Pasang Kayu.
"Kami mengimbau masyarakat yang akan melaksanakan aksi penyampaian pendapat bisa melakukan secara tertib," ujar Susatyo.
Dia pun menyampaikan agar masyarakat bisa memilih jalan alternatif untuk menghindari kepadatan kendaraan di lokasi unjuk rasa. Dia menyebut rekayasa lalu lintas akan dilakukan secara situasional.
"(Rekayasa) lalin situasional melihat eskalasi di lapangan," terangnya.
"""

# --- 2. Placeholder for the Real Embedding Function ---

def get_embedding(text: str) -> list[float]:
    """
    This is a placeholder function.
    In a real application, this function would make an API call to an embedding model
    (e.g., OpenAI, Google AI, Hugging Face).
    
    For this example, we'll return a random 8-dimensional vector.
    Real vectors are much larger (e.g., 384, 768, or 1536 dimensions).
    """
    print(f"      -> Getting embedding for chunk starting with: '{text[:30]}...'")
    # Generate a random vector and convert it to a standard Python list
    return np.random.rand(8).tolist()


# --- 3. The Processing Logic ---

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # A smaller size for this example text
    chunk_overlap=50
)

# Split the document into text chunks
print(f"--- Splitting document '{document_id}' into chunks... ---")
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
    "document_id": document_id,
    "chunks": chunk_list_for_json
}

# --- 5. Final Output and Saving ---

# Pretty-print the final JSON to the console to verify it's correct
print("\n--- Final JSON Output ---")
print(json.dumps(final_json_data, indent=2))

# Now you can save this single object to a database or file
# Example: Saving to a JSON file
output_filename = f"{document_id}.json"
with open(output_filename, 'w') as f:
    json.dump(final_json_data, f, indent=2)

print(f"\n✅ Successfully created the JSON structure and saved it to '{output_filename}'")