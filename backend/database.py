import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# --- STEP 1: LOAD ENVIRONMENT VARIABLES ---
# This function finds and loads the .env file.
load_dotenv()

# --- STEP 2: READ THE MONGO_URI VARIABLE ---
# This reads the specific MONGO_URI variable from the environment.
uri = os.getenv("MONGO_URI")

# --- STEP 3: DEBUG AND VERIFY ---
# This will prove if the steps above worked.
print("--- DATABASE CONNECTION DEBUG ---")
if uri:
    # Hide the password in the printout for security
    try:
        safe_uri_part = uri.split('@')[0]
        print(f"Connecting with URI starting with: {safe_uri_part}@...")
    except Exception:
        print("URI format is unexpected, but it was loaded.")
else:
    print("CRITICAL ERROR: The MONGO_URI variable was NOT loaded from the .env file!")
print("---------------------------------")


# --- STEP 4: CONNECT TO MONGODB ---
try:
    # Use the 'uri' variable that we loaded and verified above
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Select your database
    db = client["ILCSense_db"] # Or the name of your new database
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(f"❌ FATAL: Could not connect to MongoDB. The server will not start correctly.")
    print(f"   Error Details: {e}")
    client = None
    db = None

# Note: The dummy data insertion has been removed from here.
# It is bad practice to run database writes when a module is first imported.
# This was likely contributing to the startup failures.