import os
import sys
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

from forestCover.exception import CustomException
from forestCover.logger import logging


from forestCover.constants.database import DATABASE_COLLECTION, DATABASE_NAME


load_dotenv()
class MongoDBClient:

    def __init__(self, database_name: str):

        self.database_name = database_name
        mongo_db_uri = os.getenv("MONGO_DB_LINK")
        self.client =   MongoClient(mongo_db_uri)
        self.database = self.client[database_name]

