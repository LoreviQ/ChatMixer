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

    def __init__(self):
        load_dotenv()
        super().__init__( f"mongodb://{os.getenv("MONGODB_ADDRESS")}:27017/")

    def add_user(self, uname, platform):
        """
        Adds a user to the database

        Args:
            uname: Username of the user (String)
            platform: Name of the platform (String)

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """
        collection = self['ChatDB']['user']
        if platform == "Twitch":
            if collection.find_one({"twitch_uname": uname}):
                print("User already exists")
            else:
                user = {
                    "user": uname,
                    "twitch_uname": uname,
                    "created_date": datetime.datetime.now(tz=datetime.timezone.utc),
                }
                collection.insert_one(user)
                print("Added user")
        else:
            raise ValueError("Unsupported Platform")


if __name__ == "__main__":
    db = MDBclient()
    db.add_user("test101", "Twitch")
    db.add_user("test101", "Twitch")
    for document in db['ChatDB']['user'].find():
        print(document)
