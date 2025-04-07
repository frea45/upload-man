from pymongo import MongoClient
from config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
files_col = db["files"]

def save_file_info(user_id, url, file_name, file_size, status="uploaded"):
    data = {
        "user_id": user_id,
        "url": url,
        "file_name": file_name,
        "file_size": file_size,
        "status": status
    }
    files_col.insert_one(data)

def get_user_files(user_id):
    return list(files_col.find({"user_id": user_id}))
