import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Load environment variables
load_dotenv()

# Get MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in .env file!")

# -------------------------------
# ✅ CONNECT TO MONGODB ATLAS
# -------------------------------
def test_connection():
    """Check if MongoDB connection works."""
    print("🔄 Trying to connect...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("✅ SUCCESS! Connected to MongoDB Atlas.")
        return True
    except Exception as e:
        print("❌ FAILED to connect:")
        print(e)
        return False


# Create global client after connection test
client = MongoClient(MONGO_URI)

# -------------------------------
# ✅ DATABASE & COLLECTIONS
# -------------------------------
db = client["LinkedIn_posts_db"]        # Change if your DB name differs
influencers_col = db["influencers"]
posts_col = db["posts"]


# -------------------------------
# ✅ BASIC INSERT FUNCTIONS
# -------------------------------

def insert_influencer(data: dict):
    """Insert one influencer."""
    return influencers_col.insert_one(data)


def insert_post(data: dict):
    """Insert one processed post."""
    return posts_col.insert_one(data)


# -------------------------------
# ✅ GET DATA FUNCTIONS
# -------------------------------

def get_all_influencers():
    """Get list of all influencers."""
    return list(influencers_col.find({}, {"_id": 0}))


def get_filtered_posts(influencer=None, language=None, length=None, tag=None):
    """Fetch posts using filters."""
    query = {}

    if influencer:
        query["influencer"] = influencer
    if language:
        query["language"] = language
    if length:
        query["length"] = length
    if tag:
        query["tags"] = tag

    return list(posts_col.find(query, {"_id": 0}))

test_connection()