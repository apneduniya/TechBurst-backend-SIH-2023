"""
This module is contains the database connection class.
"""

from pymongo import MongoClient

class DBConnection:
    """
    This class is responsible for connecting to the MongoDB database and disconnecting from it.
    """
    def __init__(self, connection_url, database_name):
        self.connection_url = connection_url
        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.connection_url)
        self.db = self.client[self.database_name]
        print("\nConnected to the database")

    def disconnect(self):
        if self.client:
            self.client.close()
            print("\nDisconnected from the database")
