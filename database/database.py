
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
db.summaries.drop()
db.risk_highlights.drop()

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

# ----------------- SUMMARIES TEMPLATE -----------------
dummy_summary = {
    "contract_id": "",
    "summary": [],    # bullet list
    "created_at": None
}
s_id = db.summaries.insert_one(dummy_summary).inserted_id
db.summaries.delete_one({"_id": s_id})

# ----------------- RISKS TEMPLATE -----------------
dummy_risk = {
    "contract_id": "",
    "clause": "",
    "excerpt": "",
    "severity": "",   # low | medium | high
    "suggestion": "",
    "created_at": None
}
r_id = db.risk_highlights.insert_one(dummy_risk).inserted_id
db.risk_highlights.delete_one({"_id": r_id})

print("✅ Database initialized with templates for users, contracts (rich JSON), summaries, and risks.")