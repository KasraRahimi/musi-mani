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

    def drop_users_table(self) -> None:
        with self.__pool.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute("DROP TABLE IF EXISTS users")

    def drop_game_stats_table(self) -> None:
        with self.__pool.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute("DROP TABLE IF EXISTS game_stats")

    def create_users_table(self) -> None:
        with self.__pool.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(
                """
                CREATE TABLE users (
                    id          BIGINT UNSIGNED PRIMARY KEY,
                    name        VARCHAR(32),
                    description VARCHAR(128),
                    balance     INTEGER NOT NULL,
                    last_reward DATETIME
                )
                """
            )

    def create_posts_table(self) -> None:
        with self.__pool.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(
                """
                CREATE TABLE game_stats (
                    id          INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                    user_id     BIGINT UNSIGNED NOT NULL,
                    name        VARCHAR(128) NOT NULL,
                    date        DATETIME NOT NULL,
                    bet         INTEGER NOT NULL,
                    payout      INTEGER NOT NULL,
                    is_win      BOOLEAN NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                        ON DELETE CASCADE
                )
                """
            )

    def reset_all_data(self) -> int:
        with self.__pool.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM game_stats")
        return count[0]