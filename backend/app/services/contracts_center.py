from database import db
from datetime import datetime, timezone
from pymongo.mongo_client import MongoClient


def generate_contract_id():
    last_contract = db.contracts.find_one(
        {"contract_id": {"$regex": r"^contract-\d+$"}},
        sort=[("contract_id", -1)]
    )
    if last_contract and "contract_id" in last_contract:
        last_num = int(last_contract["contract_id"].split("-")[1])
        new_num = last_num + 1
    else:
        new_num = 1
    return f"contract-{new_num:03d}"


def create_contract(contract_data: dict):
    contract_id = generate_contract_id()
    contract_data["contract_id"] = contract_id
    contract_data["created_at"] = datetime.now(timezone.utc)
    db.contracts.insert_one(contract_data)
    print(f"✅ Contract created with id={contract_id}")
    return contract_id


def get_contract_by_id(contract_id: str):
    return db.contracts.find_one({"contract_id": contract_id}, {"_id": 0})


def list_contracts():
    return list(db.contracts.find({}, {"_id": 0}))


def update_contract(contract_id: str, updates: dict):
    updates["updated_at"] = datetime.now(timezone.utc)
    result = db.contracts.update_one({"contract_id": contract_id}, {"$set": updates})
    return result.modified_count > 0


def delete_contract(contract_id: str):
    result = db.contracts.delete_one({"contract_id": contract_id})
    return result.deleted_count > 0
