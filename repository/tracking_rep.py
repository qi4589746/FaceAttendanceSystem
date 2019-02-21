from agent.db import mongo
from domain.tracking import Tracking


def save(tracking: Tracking):
    tracking._id = mongo.db.tracking.insert_one(tracking.__dict__).inserted_id
    return tracking


def findBySubjectId(id: str):
    tracking = [doc for doc in mongo.db.tracking.find({"subjectId": id})]
    return tracking


def findAll():
    tracking = [doc for doc in mongo.db.tracking.find()]
    return tracking


def removeById(id: str):
    mongo.db.tracking.delete_one({"id": id})


def removeBySubjectId(subjectId: str):
    mongo.db.tracking.delete_many({'subjectId': subjectId})


