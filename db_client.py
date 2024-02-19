"""Connects to MongoDB Database"""

import os

import pymongo


class DB(pymongo.MongoClient):
    """
    Creates a subclass of the pymongo.MongoClient class
    Connects to MongoDB database based on .env variables
    """
    def __init__(self):
        super().__init__(f"mongodb://{os.environ.get("MONGODB_ADDRESS")}:27017/")

if __name__ == "__main__":
    db = DB()
    print(db.list_database_names())
