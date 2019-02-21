from agent.db import mongo
from domain.subject_model import SubjectModel
from agent import time_generator as tg
import repository.model_rep as modelRep


def save(subjectModel: SubjectModel):
    subjectModel._id = mongo.db.subjectModel.insert_one(subjectModel.__dict__).inserted_id
    return subjectModel


def findBySubjectId(id: str):
    subjectModel = mongo.db.subjectModel.find_one({"subjectId": id})
    return subjectModel


def findById(id: str):
    subjectModel = mongo.db.subjectModel.find_one({'id': id})
    return subjectModel


def findAll():
    subjectModel = [doc for doc in mongo.db.subjectModel.find()]
    return subjectModel


def removeById(id: str):
    mongo.db.subjectModel.delete_one({"id": id})


def removeBySubjectId(subjectId: str):
    subjectModel = findBySubjectId(subjectId)
    modelRep.removeById(subjectModel['modelId'])
    mongo.db.subjectModel.delete_one({'subjectId': subjectId})


def update(subjectModel: SubjectModel):
    message = mongo.db.subjectModel.update({'_id': subjectModel['_id']},
                                           {'$set': {'modelId': subjectModel['modelId'],
                                                     'updateTime': tg.getNowAsMilli()}},
                                           upsert=False, multi=False)
    return message
