
from datetime import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "MONGO_URI"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# --- Connect to MongoDB ---

db = client["ILCSense_db"]

# --- Drop old collections ---
"""
db.users.drop()
db.contracts.drop()
db.summaries.drop()
db.risk_highlights.drop()
"""

# ----------------- USERS TEMPLATE -----------------
dummy_user = {
    "username": "",
    "email": "",
    "role": "",       # expected: admin | doctor | manager
    "created_at": None
}
u_id = db.users.insert_one(dummy_user).inserted_id
db.users.delete_one({"_id": u_id})

# ----------------- CONTRACTS TEMPLATE (Rich JSON) -----------------
dummy_contract = {
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
c_id = db.contracts.insert_one(dummy_contract).inserted_id
db.contracts.delete_one({"_id": c_id})



dummy_embed_vector = { 
    "contract_id": "",
    "contract_name": "",
    "chunks": [
        {
        "text_content": "",
        "embedding_vector": []
        }
  ]
}
ve_id = db.embedding_vector.insert_one(dummy_embed_vector).inserted_id
db.embedding_vector.delete_one({"_id": ve_id})

print("✅ Database initialized with templates for users, contracts (rich JSON), summaries, and risks.")