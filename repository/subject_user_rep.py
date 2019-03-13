from agent.db import mongo
from domain.subject_user import SubjectUser


def save(subjectUser: SubjectUser):
    subjectUser._id = mongo.db.subjectUser.insert_one(subjectUser.__dict__).inserted_id
    return subjectUser


def findByAdminId(id: str):
    subjectUsers = [doc for doc in mongo.db.subjectUser.find({"userId": id, "role": 1})]
    return subjectUsers


def findBySubjectIdAndUserId(subjectId: str, userId: str):
    subjectUser = mongo.db.subjectUser.find_one({"subjectId": subjectId, "userId": userId, "role": 2})
    return subjectUser


def isAuthorizedBySubjectIdAndUserId(subjectId: str, userId: str):
    if mongo.db.subjectUser.find_one({"subjectId": subjectId, "userId": userId, "role": 1}) is not None:
        return True
    return False


def findBySubjectId(id: str):
    subjectUser = [doc for doc in mongo.db.subjectUser.find({"subjectId": id, "role": 2})]
    return subjectUser


def findAll():
    subjectUser = [doc for doc in mongo.db.subjectUser.find()]
    return subjectUser


def removeById(id: str):
    mongo.db.subjectUser.delete_one({"id": id})


def removeBySubjectIdAndUserId(subjectId: str, userId: str):
    mongo.db.subjectUser.delete_one({"subjectId": subjectId, "userId": userId})


def removeBySubjectId(subjectId: str):
    mongo.db.subjectUser.delete_many({'subjectId': subjectId})


def removeByUserId(userId: str):
    mongo.db.subjectUser.delete_many({'userId': userId})
