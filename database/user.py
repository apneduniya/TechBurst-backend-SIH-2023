"""
This module is responsible for managing the users collection.
"""


from pymongo import MongoClient, DESCENDING
from bson import ObjectId
from database.database import (MONGO_CONNECTION_URL, DATABASE_NAME)


# Replace this with your MongoDB collection name for users
USERS_COLLECTION_NAME = "users"

class UserDB:
    """
    This class is responsible for managing the users collection.
    """
    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION_URL)
        self.db = self.client[DATABASE_NAME]
        self.users_collection = self.db[USERS_COLLECTION_NAME]

    def create_user(self, user_data):
        """
        Inserts the user_data into the users collection.
        """
        result = self.users_collection.insert_one(user_data)
        user_id = str(result.inserted_id)
        return user_id
    
    def get_all_user(self, id, limit):
        """
        Returns the list of users with the given id and 'limit' number of rows after the given id.
        """
        if not id or id == "null":
            users_cursor = self.users_collection.find({}, {"password": False}).sort([("_id", DESCENDING)]).limit(limit) # Find the documents after the given id and get 'limit' number of rows
            users_list = list(users_cursor)
            for user in users_list:
                user["id"] = str(user["_id"])
                # user["profile_pic"] = f"https://api.earnifyy.online/get_image/{user['profile_pic_file_id']}"
                # user.pop("profile_pic_file_id")
                # user["pan_card_pic"] = f"https://api.earnifyy.online/get_image/{user['pan_card_pic_file_id']}"
                # user.pop("pan_card_pic_file_id")
                # user["aadhar_card_pic"] = f"https://api.earnifyy.online/get_image/{user['aadhar_card_pic_file_id']}"
                # user.pop("aadhar_card_pic_file_id")
            return users_list
        user = self.users_collection.find_one({"_id": ObjectId(id)}) # Find the document with the given id
        if not user:
            return None
        
        users_cursor = self.users_collection.find({"_id": {"$lt": ObjectId(id)}}).sort([("_id", DESCENDING)]).limit(limit) # Find the documents after the given id and get 'limit' number of rows
        users_list = list(users_cursor)
        for user in users_list:
            user["id"] = str(user["_id"])
            # user["profile_pic"] = f"https://api.earnifyy.online/get_image/{user['profile_pic_file_id']}"
            # user.pop("profile_pic_file_id")
            # user["pan_card_pic"] = f"https://api.earnifyy.online/get_image/{user['pan_card_pic_file_id']}"
            # user.pop("pan_card_pic_file_id")
            # user["aadhar_card_pic"] = f"https://api.earnifyy.online/get_image/{user['aadhar_card_pic_file_id']}"
            # user.pop("aadhar_card_pic_file_id")
        return users_list

    def get_user(self, user_id):
        """
        Returns the user with the given user_id.
        """
        user = self.users_collection.find_one({"_id": ObjectId(user_id)})
        return user
    
    def get_user_email(self, email):
        """
        Returns the user with the given email.
        """
        user = self.users_collection.find_one({"email": email})
        return user
    
    def add_balance(self, user_id, amount):
        """
        Adds the given amount to the user's balance.
        """
        self.users_collection.update_one({"_id": ObjectId(user_id)}, {"$inc": {"balance": amount}})

    def deduct_balance(self, user_id, amount):
        """
        Deducts the given amount from the user's balance.
        """
        self.users_collection.update_one({"_id": ObjectId(user_id)}, {"$inc": {"balance": -amount}})

    