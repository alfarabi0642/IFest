import os
from openai import AzureOpenAI
import json
from copy import deepcopy
import re
from database import db
from datetime import datetime, timezone

OUTPUT_DIR = "output"
JSON_OUTPUT_DIR = "json"
contract_text = ""

txt_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".txt")]
for file in txt_files:
    doc_name = os.path.splitext(file)[0]
    file_path = os.path.join(OUTPUT_DIR, file)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        contract_text += f.read() + "\n"

endpoint = "https://13524-mfzrpl5t-eastus2.cognitiveservices.azure.com/"
model_name = "gpt-5-mini"
deployment = "gpt-5-mini"

subscription_key = "9WDekKj2uGYShRDLRaKxuuA8UIadSFI2MsmnL5sx4FjQPq71jHMBJQQJ99BIACHYHv6XJ3w3AAAAACOGRfpl"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

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

# --- Prompt instructing AI to return schema ---
prompt = f"""
You are a contract analysis assistant.
Read the contract text and return valid JSON strictly matching this schema:

{json.dumps(SCHEMA_TEMPLATE, indent=2)}

Contract:
{contract_text}
"""

# --- Call Azure OpenAI ---
resp = client.chat.completions.create(
    model=deployment,
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=2000  # <-- correct parameter
)

def extract_json(text: str, fallback_schema: dict):
    """
    Try to extract valid JSON from model output.
    If parsing fails, return the fallback schema.
    """
    try:
        # 1. Grab first {...} block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in response")

        raw_json = match.group(0)

        # 2. Attempt to parse
        return json.loads(raw_json)

    except Exception as e:
        print("AI output not valid JSON, using fallback:", e)
        return fallback_schema

# --- Parse safely ---
def deep_merge(template, data):
    if isinstance(template, dict):
        merged = {}
        for k, v in template.items():
            if k in data:
                merged[k] = deep_merge(v, data[k])
            else:
                merged[k] = v
        return merged
    elif isinstance(template, list):
        if isinstance(data, list) and len(data) > 0:
            return [deep_merge(template[0], data[0])]
        else:
            return template
    else:
        return data if data not in [None, ""] else template
    
try:
    ai_output = extract_json(resp.choices[0].message.content, SCHEMA_TEMPLATE)
    final_doc = deep_merge(SCHEMA_TEMPLATE, ai_output)
except Exception as e:
    print("AI output not valid JSON, fallback to empty schema:", e)
    ai_output = {}
# --- Merge with schema (fill missing fields) ---
def deep_merge(template, data):
    if isinstance(template, dict):
        merged = {}
        for k, v in template.items():
            if k in data:
                merged[k] = deep_merge(v, data[k])
            else:
                merged[k] = v
        return merged
    elif isinstance(template, list):
        if isinstance(data, list) and len(data) > 0:
            return [deep_merge(template[0], data[0])]
        else:
            return template
    else:
        return data if data not in [None, ""] else template

final_doc = deep_merge(SCHEMA_TEMPLATE, ai_output)

# ---------------- Auto-generate Contract ID ----------------
next_id = db.contracts.count_documents({}) + 1
document_id = f"DOC{next_id:04d}"  # e.g., DOC0001, DOC0002

now = datetime.now(timezone.utc)
final_doc["contractMetadata"]["documentId"] = document_id
final_doc["contractMetadata"]["documentTitle"] = "Master Services Agreement"
final_doc["contractMetadata"]["documentType"] = "MSA"
final_doc["contractMetadata"]["processingTimestamp"] = now.isoformat()

# ---------------- Insert into MongoDB ----------------
# 1. Main contracts collection
db.contracts.insert_one({
    "raw_text": contract_text,
    "analysis": final_doc,
    "created_at": now
})

# 2. Summaries collection (cross-reference)

print(f"Contract {document_id} inserted into contracts, summaries, and risks!")

print("Final structured contract JSON:")
print(json.dumps(final_doc, indent=2))