"""Connects to MongoDB Database"""

import datetime
import os

import pymongo
from dotenv import load_dotenv


class MDBclient(pymongo.MongoClient):
    """
    Creates a subclass of the pymongo.MongoClient class
    Connects to MongoDB database based on .env variables
    """

    def __init__(self, database = 'ChatDB'):
        load_dotenv()
        super().__init__( f"mongodb://{os.getenv("MONGODB_ADDRESS")}:27017/")
        self.db = database

    def add_user(self, uname, platform):
        """
        Adds a user to the 'users' collection in the 'self.db' database

        Args:
            uname: Username of the user (String)
            platform: Name of the platform (String)

        Returns:
            _id = UID of the user added (or found if already exists)

        Raises:
            ValueError: If platform does not match a supported platform
        """
        collection = self[self.db]['users']
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        if platform == "Twitch":
            if collection.find_one({"twitch_uname": uname}):
                _id = collection.find_one({"twitch_uname": uname})["_id"]
                collection.update_one(
                    {"_id": _id},
                    {"$set": {"updated_date": now}}
                )
            else:
                user_document = {
                    "user": uname,
                    "twitch_uname": uname,
                    "created_date": now,
                    "updated_date": now
                }
                _id = collection.insert_one(user_document).inserted_id
            return _id
        raise ValueError("Unsupported Platform")

    def add_message(self, uname, platform, message):
        """
        Adds a message to the 'messages' collection in the 'self.db' database

        Args:
            uname: Username of the user (String)
            platform: Name of the platform (String)
            message: Contents of the message (String)
        """
        _id = self.add_user(uname, platform)
        collection = self[self.db]['messages']
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        message_document = {
            "user_id": _id,
            "content": message,
            "platform": platform,
            "date": now
        }
        collection.insert_one(message_document)


if __name__ == "__main__":
    db = MDBclient()
    db.add_message("test102", "Twitch", "wow so cool")
    for document in db[db.db]['users'].find():
        print(document)
    for document in db[db.db]['messages'].find():
        print(document)
