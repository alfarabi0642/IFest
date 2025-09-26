import os
import json
import re
from datetime import datetime, timezone
from openai import AzureOpenAI
from database import db
from .embedding_service import create_and_store_embeddings # Import our refactored function

# --- Initialize Azure Client ---
client = AzureOpenAI(
    api_key=os.getenv("AZURE_CHAT_KEY"),
    api_version="2024-02-01", # Use a stable API version
    azure_endpoint=os.getenv("AZURE_CHAT_ENDPOINT")
)
DEPLOYMENT_NAME = os.getenv("AZURE_CHAT_DEPLOYMENT")

# --- Schema Template (remains the same) ---
SCHEMA_TEMPLATE = {
    "contractMetadata": {
        "documentId": "",
        "documentTitle": "",
        "documentType": "",
        "processingTimestamp": None
    },
    "contractSummarization": {
        "executiveSummary": "",
        "parties": [
            {"name": "", "role": "", "contactInfo": ""}
        ],
        # --- NEW FIELDS ADDED HERE ---
        "contractValue": "",          # e.g., "IDR 20.000.000", "USD 5,000 / month"
        "contractPeriod": "",         # e.g., "1 Sep - 1 Okt 2025", "3 years from signing"
        "contractStatus": "",         # e.g., "Approved", "Under Review", "Unapproved"
        "contractLocation": "",       # e.g., "Bandung, Indonesia", "Jakarta"
        # ---------------------------
        "keyTerms": [
            {"term": "", "definition": ""}
        ],
        "governingLaw": "",
        "jurisdiction": ""
    },
    "clauseLevelRiskAndCompliance": {
        "clauses": [
            {
                "clauseId": "",
                "clauseTitle": "",
                "clauseText": "",
                "riskAnalysis": {
                    "riskLevel": "",
                    "riskCategory": "",
                    "riskDescription": ""
                },
                "complianceSuggestions": [""]
            }
        ]
    },
    "lifecycleMonitoring": {
        "keyDatesAndEvents": [
            {"eventName": "", "date": None, "description": ""}
        ],
        "renewalInformation": {
            "renewalType": "",
            "renewalTerm": "",
            "noticePeriodDays": None
        },
        "obligations": [
            {
                "obligatedParty": "",
                "obligationDescription": "",
                "frequency": "",
                "nextDueDate": None
            }
        ]
    }
}

def analyze_contract_text(contract_text: str, contract_name: str) -> str:
    """
    Analyzes contract text, stores results and embeddings in DB, and returns the document ID.
    """
    prompt = f"""
    You are a contract analysis assistant.  
    Your task: extract structured information from the contract.  

    Rules:  
    1. Output must be a single valid JSON object.  
    2. JSON must exactly follow the provided schema (all keys must appear).  
    3. If information is missing, use null. 
    4. Do not add explanations or extra text outside JSON.
    5. On "ContractValue" only uses Rp, Numbers, and separate thousands (3 digits).
    6. On "ContractPeriod" only uses format <tanggal bulan> - <tanggal bulan>.
    7. riskCategory is the specific type or nature of the risk (e.g., Financial, Legal, Operational).
    8. riskLevel is the severity of the risk, color-coded for quick identification. Only filled with "Green" for low risk, "Yellow" for medium risk, and "Red" for high risk

    {json.dumps(SCHEMA_TEMPLATE, indent=2)}

    Contract:
    {contract_text}
    """
    
    resp = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"} # Use JSON mode for reliability
    )
    
    try:
        ai_output = json.loads(resp.choices[0].message.content)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing AI JSON output: {e}. Using empty schema.")
        ai_output = {}

    # Auto-generate Contract ID
    next_id = db.contracts.count_documents({}) + 1
    document_id = f"DOC{next_id:04d}"
    now = datetime.now(timezone.utc)
    
    # Populate metadata
    final_doc = ai_output # Start with AI output
    final_doc.setdefault("contractMetadata", {})
    final_doc["contractMetadata"]["documentId"] = document_id
    final_doc["contractMetadata"]["documentTitle"] = contract_name
    final_doc["contractMetadata"]["processingTimestamp"] = now.isoformat()
    
    # --- Store analysis in the main 'contracts' collection ---
    db.contracts.insert_one({
        "_id": document_id,
        "raw_text": contract_text,
        "analysis": final_doc,
        "created_at": now
    })
    print(f"Contract {document_id} analysis inserted into database.")

    # --- Generate and store embeddings ---
    create_and_store_embeddings(document_id, contract_name, contract_text)
    
    return document_id