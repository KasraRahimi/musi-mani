from constants import DATE_FORMAT
from models.game_stat import GameStat
from models.user_info import UserInfo
from database.sql_db import SQLDb
from datetime import datetime, timedelta

USER_TABLE_NAME = "users"
GAME_STATS_TABLE_NAME = "game_stats"


class BotUser:
    __db = SQLDb()

    def __init__(self, user_id: str):
        self.user_id = int(user_id)
        self.__create_new_user()

    def __create_new_user(self):
        if self.get_user_info():
            return
        with self.__db.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(f"INSERT INTO {USER_TABLE_NAME} (id, balance) VALUES (%s, %s)", (self.user_id, 0))
            cnx.commit()


    def get_user_info(self) -> UserInfo | None:
        with self.__db.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(f"SELECT * FROM {USER_TABLE_NAME} WHERE id=%s", (self.user_id,))
            user_data = cursor.fetchone()
            cursor.execute(
                f"SELECT user_id, name, date, bet, payout, is_win FROM {GAME_STATS_TABLE_NAME} WHERE user_id=%s",
                (self.user_id,)
            )
            game_stats_data = cursor.fetchall()
        game_stats = list(map(GameStat.from_sql_tuple, game_stats_data))
        if user_data:
            user_info = UserInfo.from_sql_tuple(user_data, game_stats)
        else:
            user_info = None
        return user_info

    @property
    def balance(self) -> int | None:
        user_info = self.get_user_info()
        if user_info:
            return user_info.balance
        return None

    @property
    def last_reward(self) -> datetime | None:
        user_info = self.get_user_info()
        if user_info:
            return user_info.last_reward
        return None

    @property
    def name(self) -> str | None:
        user_info = self.get_user_info()
        if user_info:
            return user_info.name
        return None

    def set_name(self, new_name: str) -> None:
        with self.__db.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(f"UPDATE {USER_TABLE_NAME} SET name=%s WHERE id=%s", (new_name, self.user_id))
            cnx.commit()

    @property
    def description(self) -> str | None:
        user_info = self.get_user_info()
        if user_info:
            return user_info.description
        return None

    def set_description(self, new_description: str) -> None:
        with self.__db.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(f"UPDATE {USER_TABLE_NAME} SET description=%s WHERE id=%s", (new_description, self.user_id))
            cnx.commit()

    @property
    def game_stats(self) -> list[GameStat]:
        user_info = self.get_user_info()
        if user_info:
            return user_info.game_stats
        return []

    def __increment_balance(self, amount: int):
        with self.__db.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(f"UPDATE {USER_TABLE_NAME} SET balance=balance+%s WHERE id=%s", (amount, self.user_id))
            cnx.commit()

    def deposit(self, amount: int):
        if amount < 0:
            raise ValueError("deposit amount should be positive")
        self.__increment_balance(amount)

    def withdraw(self, amount: int):
        if amount < 0:
            raise ValueError("withdraw amount should be positive")
        if self.balance < amount:
            raise ValueError("insufficient funds to withdraw amount")

        self.__increment_balance(-amount)

    def time_since_last_reward(self) -> None | timedelta:
        last_reward = self.last_reward
        if last_reward is None:
            return last_reward

        now = datetime.now()
        delta = now - last_reward
        return delta

    def claim_reward(self, reward_amount: int):
        now_string = datetime.now().strftime(DATE_FORMAT)
        with self.__db.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(f"UPDATE {USER_TABLE_NAME} SET last_reward=%s WHERE id=%s", (now_string, self.user_id))
            cnx.commit()
        self.deposit(reward_amount)

    def add_game_stat(self, game_stat: GameStat) -> None:
        game_stat.user_id = self.user_id
        game_stat_tuple = game_stat.to_sql_tuple()
        with self.__db.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute(f"INSERT INTO {GAME_STATS_TABLE_NAME} (user_id, name, date, bet, payout, is_win) VALUES (%s, %s, %s, %s, %s, %s)", game_stat_tuple)


if __name__ == "__main__":
    me = BotUser(22218595743105024)
    print(me.get_user_info().game_stats)
    new_game_stat = GameStat("Test", datetime.now(), 10, 0, False)
    me.add_game_stat(new_game_stat)
    print(
        me.get_user_info().game_stats
    )