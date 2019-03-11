from agent import time_generator as tg
from agent.db import mongo
from domain.user import User


def save(user: User):
    user._id = mongo.db.user.insert_one(user.__dict__).inserted_id
    return user


def findById(id: str):
    user = mongo.db.user.find_one({"id": id})
    return user


def findAll():
    users = [doc for doc in mongo.db.user.find()]
    return users


def removeById(id: str):
    mongo.db.user.delete_one({"id": id})


def update(user: User):
    messqge = mongo.db.user.update({"_id": user['_id']},
                                {'$set': {'name': user['name'], 'updateTime': tg.getNowAsMilli()}},
                                upsert=False, multi=False)
    return user
