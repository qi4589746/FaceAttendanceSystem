from agent.db import mongo
from domain.user_image import UserImage
import repository.image_rep as imageRep


def save(userImage: UserImage):
    userImage._id = mongo.db.userImage.insert_one(userImage.__dict__).inserted_id
    return userImage


def findById(id: str):
    userImage = mongo.db.userImage.find_one({"id": id})
    return userImage


def findByUserId(id: str):
    userImages = [doc for doc in mongo.db.userImage.find({"userId": id})]
    return userImages


def findAll():
    userImages = [doc for doc in mongo.db.userImage.find()]
    return userImages


def removeById(id: str):
    mongo.db.userImage.delete_one({"id": id})


def removeByUserId(userId: str):
    userImages = findByUserId(userId)
    for userImage in userImages:
        imageRep.removeById(userImage['imageId'])
    mongo.db.userImage.delete_many({'userId': userId})
