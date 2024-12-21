from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from constants import DB_NAME, DB_USERNAME, DB_PASSWORD
import mysql.connector as sql

SQL_CONFIG = {
    "host": "localhost",
    "user": DB_USERNAME,
    "password": DB_PASSWORD,
    "database": DB_NAME,
}

class SQLDb:
    __instance = None
    __pool = None

    def __new__(cls):
        if cls.__instance is None:
            print("Creating instance of database")
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialize()
        return cls.__instance

    def __initialize(self):
        self.__pool = sql.pooling.MySQLConnectionPool(
            pool_size=5,
            pool_name="musi_mani_pool",
            autocommit=True,
            **SQL_CONFIG
        )

    def get_connection(self) -> MySQLConnectionAbstract | PooledMySQLConnection:
        return self.__pool.get_connection()

