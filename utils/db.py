from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv() 

def get_database():
    connection_string = os.getenv("MONGO_URI")
    if not connection_string:
        raise ValueError("MONGO_URI is not set in environment variables.")
    client = MongoClient(connection_string)
    return client["test"]
