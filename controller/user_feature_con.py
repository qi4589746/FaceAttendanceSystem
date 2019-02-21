from flask import Blueprint, request
from agent import id_generator as ig
from agent import time_generator as tg
from flask_api import status
from bson import json_util
from domain.user_feature import UserFeature
import repository.user_feature_rep as userFeatureRep
import agent.content_type as ContentType

mod = Blueprint('user_feature_controller', __name__, url_prefix='/userFeatureController')


def createUserFeature(userId: str, imageId: str, feature):
    userFeature = UserFeature(id=ig.generateId('userFeature'), userId=userId, imageId=imageId, feature=feature,
                              createTime=tg.getNowAsMilli())
    userFeature = userFeatureRep.save(userFeature)
    return userFeature


# def getUserFeatureByImageId(imageId: str):
#     userFeature = userFeatureRep.findByImageId(imageId)
#     return userFeature


@mod.route('userFeatures', methods=['GET'])
def getUserFeatureByUserId():
    userId = request.json['userId']
    userFeatures = userFeatureRep.findByUserId(userId)
    return json_util.dumps({'userFeatures': userFeatures}), status.HTTP_200_OK, ContentType.json


# def removeUserFeatureById(id: str):
#     userFeatureRep.removeById(id=id)
#     return id
