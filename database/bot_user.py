import asyncio

from .mongo_database import BotDatabase
from datetime import datetime, timedelta

COLLECTION_NAME = "users"

class BotUser:
    __collection = BotDatabase().get_collection(COLLECTION_NAME)

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.__create_new_user()

    def __create_new_user(self):
        if self.__find_user() is None:
            self.__collection.insert_one({
                "_id": self.user_id,
                "last_reward": None,
                "balance": 0,
            })

    def __find_user(self):
        return self.__collection.find_one({"_id": self.user_id})

    @property
    def balance(self):
        return self.__find_user().get("balance")

    @property
    def last_reward(self) -> datetime | None:
        return self.__find_user().get("last_reward")

    @property
    def name(self) -> str | None:
        return self.__find_user().get("name")

    def set_name(self, new_name: str) -> None:
        self.__collection.update_one(
            {"_id": self.user_id},
            {"$set": {"name": new_name}}
        )

    @property
    def description(self) -> str | None:
        return self.__find_user().get("description")

    def set_description(self, new_description: str) -> None:
        self.__collection.update_one(
            {"_id": self.user_id},
            {"$set": {"description": new_description}}
        )


    def __increment_balance(self, amount: int):
        self.__collection.update_one(
            {"_id": self.user_id},
            {"$inc": {"balance": amount}}
        )

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
        self.deposit(reward_amount)
        self.__collection.update_one(
            {"_id": self.user_id},
            {"$set": {"last_reward": datetime.now()}}
        )
