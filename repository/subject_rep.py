from agent import time_generator as tg
from agent.db import mongo
from domain.subject import Subject


def save(subject:Subject):
    subject._id = mongo.db.subject.insert_one(subject.__dict__).inserted_id
    return subject


def findById(id: str):
    subject = mongo.db.subject.find_one({"id": id})
    return subject


def findAll():
    subject = [doc for doc in mongo.db.subject.find()]
    return subject


def removeById(id: str):
    mongo.db.subject.delete_one({"id": id})


def update(subject: Subject):
    message = mongo.db.subject.update({'_id': subject['_id']},
                                      {'$set': {'name': subject['name'],
                                                     'updateTime': tg.getNowAsMilli()}},
                                      upsert=False)
    return message
