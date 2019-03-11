from agent.db import mongo
from domain.model import Model


def save(model: Model):
    model._id = mongo.db.model.insert_one(model.__dict__).inserted_id
    return model


def findById(id: str):
    model = mongo.db.model.find_one({"id": id})
    return model


def removeById(id: str):
    mongo.db.model.delete_one({"id": id})
