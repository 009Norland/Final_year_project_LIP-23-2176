"""src/database/mongo_client.py — MongoDB Atlas connection manager."""
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config.settings import MONGO_URI, MONGO_DB_NAME, COLLECTIONS

logger = logging.getLogger(__name__)
_client = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        logger.info("Connected to MongoDB: %s", MONGO_DB_NAME)
    return _client

def get_db():
    return get_client()[MONGO_DB_NAME]

def insert_one(col, doc):
    result = get_db()[COLLECTIONS[col]].insert_one(doc)
    return str(result.inserted_id)

def find_one(col, query):
    return get_db()[COLLECTIONS[col]].find_one(query)

def find_many(col, query={}, limit=0):
    cursor = get_db()[COLLECTIONS[col]].find(query)
    if limit: cursor = cursor.limit(limit)
    return list(cursor)

def update_one(col, query, update):
    result = get_db()[COLLECTIONS[col]].update_one(query, {"$set": update})
    return result.modified_count
