
# IntelliContract AI 📄✨

ILCSense AI is a full-stack web application designed to streamline contract management. It leverages Optical Character Recognition (OCR) to digitize PDF documents and utilizes Large Language Models (LLMs) from Azure OpenAI to perform deep analysis, summarization, and risk assessment. The standout feature is a powerful semantic search capability that allows users to ask natural language questions across their entire contract library.

## Key Features

  * *PDF Contract Upload*: Easily upload contract documents in PDF format.
  * *Automated OCR*: Automatically extracts text from scanned or image-based PDFs using Tesseract.
  * *AI-Powered Analysis*: For each contract, the system automatically generates:
      * An executive summary.
      * A list of involved parties.
      * Key terms and definitions.
      * Clause-by-clause risk analysis and compliance suggestions.
  * *Semantic Search: A powerful search bar that understands the *meaning behind your query, not just keywords, to find the most relevant contracts.
  * *Responsive UI*: A clean, modern interface built with React and Tailwind CSS for managing and viewing contracts.


## 🖼 Screenshots


The main dashboard displaying a list of uploaded contracts.

<img width="1365" height="600" alt="image" src="https://github.com/user-attachments/assets/1ffc4a48-2f16-4016-8d23-3361b59f4658" />

The details view providing an in-depth AI analysis of a selected contract.

-----

## 🛠 Tech Stack

| Category      | Technology                                                                          |
|---------------|-------------------------------------------------------------------------------------|
| *Frontend* | React, Vite, Tailwind CSS, Axios                                                    |
| *Backend* | Python 3, FastAPI                                                                  |
| *Database* | MongoDB Atlas (with Vector Search)                                                  |
| *AI Services* | Azure OpenAI (for GPT-4/equivalent models and text-embedding-3-large)            |
| *OCR* | Tesseract, ImageMagick                                                              |
| *Python Libs*| PyMongo, Uvicorn, OpenAI, LangChain (for text splitting), python-dotenv, python-multipart |

-----

## ⚙ Prerequisites

Before you begin, ensure you have the following installed on your system:

  * Python (3.9+)
  * Node.js and npm
  * Git
  * *Tesseract-OCR*: [Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)
  * *ImageMagick*: [Installation Guide](https://imagemagick.org/script/download.php) (During installation, make sure to check the box to "Add application directory to your system path (PATH)").

You will also need accounts for:

  * [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (with a free M0 cluster created)
  * [Microsoft Azure](https://azure.microsoft.com/) (with access to OpenAI services)

-----

## 🚀 Getting Started

### 1\. Clone the Repository

bash
git clone https://your-repo-url/IntelliContract-AI.git
cd IntelliContract-AI


### 2\. Backend Setup

First, navigate to the backend directory and set up the environment.

bash
cd backend


*a. Create and activate a virtual environment:*

bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate


*b. Install Python dependencies:*

bash
pip install -r requirements.txt


*c. Set up environment variables:*
Create a file named .env in the backend directory and fill it with your credentials.

ini
# .env.example

# --- MongoDB Configuration ---
# Use the long, "Standard Connection String" from Atlas
MONGO_URI="mongodb://user:password@ac-....mongodb.net..."

# --- Azure Embedding Model ---
AZURE_EMBEDDING_KEY="your-embedding-service-api-key"
AZURE_EMBEDDING_ENDPOINT="https://your-embedding-resource.openai.azure.com/"
AZURE_EMBEDDING_DEPLOYMENT="name-of-your-embedding-deployment" # e.g., text-embedding-3-large

# --- Azure Chat Model ---
AZURE_CHAT_KEY="your-chat-service-api-key"
AZURE_CHAT_ENDPOINT="https://your-chat-resource.openai.azure.com/"
AZURE_CHAT_DEPLOYMENT="name-of-your-chat-model-deployment" # e.g., gpt-4


*d. Set up the MongoDB Vector Search Index:*
In your MongoDB Atlas dashboard, create a Vector Search Index on the contract_chunks collection (this collection will be created automatically on the first upload).

  * *Index Name*: vector_index
  * *JSON Definition*:
    json
    {
      "fields": [
        {
          "type": "vector",
          "path": "embedding_vector",
          "numDimensions": 3072,
          "similarity": "cosine"
        },
        {
          "type": "filter",
          "path": "contract_id"
        }
      ]
    }
    

### 3\. Frontend Setup

In a new terminal, navigate to the frontend directory.

bash
cd frontend


*Install Node.js dependencies:*

bash
npm install


### 4\. Running the Application

You need to have both the backend and frontend servers running simultaneously.

  * *To run the backend server* (from the backend directory):

    bash
    uvicorn main:app --reload
    

    The API will be available at http://127.0.0.1:8000.

  * *To run the frontend server* (from the frontend directory):

    bash
    npm run dev
    

    The web application will be available at http://localhost:5173.

-----

## Endpoints API

Here are the main API endpoints available:

| Method | Path                            | Description                                           |
|--------|---------------------------------|-------------------------------------------------------|
| POST | /contracts/upload             | Uploads a new PDF contract for processing.            |
| GET  | /contracts                    | Retrieves a summary list of all contracts.            |
| GET  | /contracts/{document_id}      | Retrieves the full AI analysis for a single contract. |
| GET  | /contracts/search             | Performs a semantic search across all contracts.      |
| POST | /contracts/{document_id}/query| Asks a specific question about a single contract (RAG).|
