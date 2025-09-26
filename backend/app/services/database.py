
from datetime import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://fikriisawsome_db_user:123432@cluster0.xfef0fo.mongodb.net/hackathon_db?retryWrites=true&w=majority"


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
db.users.drop()
db.contracts.drop()
db.vector_store.drop()


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

dummy_vec = {
        "documentId": "",
        "embedding": [],
        
    }

v_id = db.vector_store.insert_one(dummy_vec).inserted_id
db.vector_store.delete_one({"_id": v_id})

