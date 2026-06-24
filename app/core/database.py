from pymongo import MongoClient

from app.core.config import COLLECTION_NAME, DB_NAME, MONGO_URI

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def get_properties_collection():
    return db[COLLECTION_NAME]
