"""Database client connection"""

from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(getenv("DATABASE_URI"))
database = client[getenv("DATABASE_NAME")]
