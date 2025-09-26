from datetime import datetime, timezone
from pymongo import MongoClient
from database import db
from fastapi import HTTPException

current_user = None

def generate_user_id():
    """Generate incremental user_id like user-001, user-002"""
    last_user = db.users.find_one(
        {"user_id": {"$regex": r"^user-\d+$"}},
        sort=[("user_id", -1)]
    )
    if last_user and "user_id" in last_user:
        last_num = int(last_user["user_id"].split("-")[1])
        new_num = last_num + 1
    else:
        new_num = 1
    return f"user-{new_num:03d}"

def add_user(username, email, role, password):
    if db.users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if role not in ["admin", "staff", "manager"]:
        raise HTTPException(status_code=400, detail="Invalid role specified")

    user_id = generate_user_id()
    user = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "role": role,
        "password": password,
        "created_at": datetime.now(timezone.utc)
    }
    db.users.insert_one(user)
    print(f"✅ User {username} added with role={role}, id={user_id}")
    return user_id

def login(username, password):
    global current_user
    user = db.users.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if password == user.get("password"):
        current_user = user
        return {
            "success": True,
            "role": user["role"],
            "user_id": user["user_id"],
            "message": f"Welcome {username}"
        }
    raise HTTPException(status_code=401, detail="Invalid password")

def logout():
    global current_user
    if current_user is None:
        return {"message": "No user is currently logged in."}
    current_user = None
    return {"message": "👋 Logged out successfully"}

def get_user_by_id(user_id: str):
    user = db.users.find_one({"user_id": user_id}, {"_id": 0, "password": 0})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    return user

def list_users():
    return list(db.users.find({}, {"_id": 0, "password": 0}))

def update_user(user_id: str, updates: dict):
    # Prevent password from being updated directly via this generic endpoint
    if 'password' in updates:
        del updates['password']
    updates["updated_at"] = datetime.now(timezone.utc)
    result = db.users.update_one({"user_id": user_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found or no new data provided")
    return {"message": f"User {user_id} updated successfully."}

def delete_user(user_id: str):
    result = db.users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    return {"message": f"User {user_id} deleted successfully."}


def create_admin():
    if db.users.find_one({"role": "admin"}):
        print("⚠ Admin already exists")
        return
    
    admin_user = {
        "user_id": generate_user_id(),
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "password": "admin123",
        "created_at": datetime.now(timezone.utc)
    }
    db.users.insert_one(admin_user)
    print(f"✅ Admin user created with username=admin, password=admin123, id={admin_user['user_id']}")

