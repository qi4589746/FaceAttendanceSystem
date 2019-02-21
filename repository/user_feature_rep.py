from agent.db import mongo
from domain.user_feature import UserFeature


def save(userFeature: UserFeature):
    userFeature._id = mongo.db.userFeature.insert_one(userFeature.__dict__).inserted_id
    return userFeature


def findByUserId(userId: str):
    userFeatures = [doc for doc in mongo.db.userFeature.find({"userId": userId})]
    return userFeatures


def findByImageId(imageId: str):
    userFeature = mongo.db.userFeature.find_one({"imageId": imageId})
    return userFeature


def findAll():
    userFeature = [doc for doc in mongo.db.userFeature.find()]
    return userFeature


def removeById(id: str):
    mongo.db.userFeature.delete_one({"id": id})


def removeByUserId(userId: str):
    mongo.db.userFeature.delete_many({'userId': userId})
