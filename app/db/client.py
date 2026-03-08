from pymongo import MongoClient

from app.core.config import settings

db_client = MongoClient(settings.mongo_uri)
db = db_client[settings.mongo_db_name]
