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

    def add_user(self, uname, platform, timestamp):
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
        platforms = {
            "Twitch": "twitch_uname",
            "Discord": "discord_uname",
            "Youtube": "youtube_uname"
        }
        if platform in platforms:
            collection = self[self.db]['users']
            if collection.find_one({platforms[platform]: uname}):
                _id = collection.find_one({platforms[platform]: uname})["_id"]
                collection.update_one(
                    {"_id": _id},
                    {"$set": {"updated_date": timestamp}}
                )
            else:
                user_document = {
                    "user": uname,
                    platforms[platform]: uname,
                    "created_date": timestamp,
                    "updated_date": timestamp
                }
                _id = collection.insert_one(user_document).inserted_id
            return _id
        raise ValueError("Unsupported Platform")

    def add_message(self, uname, platform, message, timestamp=datetime.datetime.now(tz=datetime.timezone.utc)):
        """
        Adds a message to the 'messages' collection in the 'self.db' database

        Args:
            uname: Username of the user (String)
            platform: Name of the platform (String)
            message: Contents of the message (String)
        """
        _id = self.add_user(uname, platform, timestamp)
        collection = self[self.db]['messages']
        message_document = {
            "user_id": _id,
            "content": message,
            "platform": platform,
            "date": timestamp
        }
        collection.insert_one(message_document)


if __name__ == "__main__":
    db = MDBclient()
    db.add_message("test102", "Twitch", "wow so cool")
    for document in db[db.db]['users'].find():
        print(document)
    for document in db[db.db]['messages'].find():
        print(document)
