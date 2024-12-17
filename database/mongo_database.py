from pymongo import MongoClient
from constants import MONGO_DB_URI

DATABASE_NAME = "musi-mani"


class BotDatabase:
    __instance = None

    __client = None
    __database = None

    def __new__(cls):
        if cls.__instance is None:
            print("Creating instance of database")
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialize()
        return cls.__instance

    def __initialize(self):
        self.__client = MongoClient(MONGO_DB_URI)
        self.__database = self.__client.get_database(DATABASE_NAME)

    @property
    def db(self):
        return self.__database

    def get_collection(self, collection_name: str):
        return self.__database.get_collection(collection_name)
