from datetime import datetime, timezone
from pymongo import MongoClient
from database import db

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
    return f"user-{new_num:03d}"  # pad with 3 digits


def add_user(username, email, role, password):
    if role not in ["admin", "staff", "manager"]:
        raise ValueError("Invalid role")

    user_id = generate_user_id()
    user = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "role": role,
        "password": password,  # plaintext for hackathon only
        "created_at": datetime.now(timezone.utc)
    }
    db.users.insert_one(user)
    print(f"✅ User {username} added with role={role}, id={user_id}")
    return user_id


def require_role(allowed_roles):
    def wrapper(func):
        def inner(*args, **kwargs):
            global current_user
            if not current_user:
                return "❌ Access denied: No user logged in"
            if current_user["role"] not in allowed_roles:
                return f"❌ Access denied: {current_user['role']} cannot perform this action"
            return func(*args, **kwargs)
        return inner
    return wrapper


def create_admin():
    if db.users.find_one({"role": "admin"}):
        print("⚠️ Admin already exists")
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


def login(username, password):
    global current_user
    user = db.users.find_one({"username": username})
    if not user:
        return {"success": False, "message": "User not found"}
    
    if password == user.get("password"):
        current_user = user
        return {
            "success": True,
            "role": user["role"],
            "user_id": user["user_id"],
            "message": f"Welcome {username}"
        }
    
    return {"success": False, "message": "Invalid password"}


def logout():
    global current_user
    current_user = None
    return "👋 Logged out"


# ----------------- USER CRUD -----------------

def create_user(username, email, role, password):
    return add_user(username, email, role, password)


def get_user_by_id(user_id: str):
    return db.users.find_one({"user_id": user_id}, {"_id": 0})


def list_users():
    return list(db.users.find({}, {"_id": 0}))


def update_user(user_id: str, updates: dict):
    updates["updated_at"] = datetime.now(timezone.utc)
    result = db.users.update_one({"user_id": user_id}, {"$set": updates})
    return result.modified_count > 0


def delete_user(user_id: str):
    result = db.users.delete_one({"user_id": user_id})
    return result.deleted_count > 0
