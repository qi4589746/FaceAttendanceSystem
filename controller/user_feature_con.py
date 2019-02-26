from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.user_feature_rep as userFeatureRep
from agent import id_generator as ig
from agent import time_generator as tg
from domain.user_feature import UserFeature

mod = Blueprint('user_feature_controller', __name__, url_prefix='/userFeatureController')


def createUserFeature(userId: str, imageId: str, feature):
    userFeature = UserFeature(id=ig.generateId('userFeature'), userId=userId, imageId=imageId, feature=feature,
                              createTime=tg.getNowAsMilli(), updateTime=tg.getNowAsMilli())
    userFeature = userFeatureRep.save(userFeature)
    return userFeature


# def getUserFeatureByImageId(imageId: str):
#     userFeature = userFeatureRep.findByImageId(imageId)
#     return userFeature


@mod.route('/userFeatures', methods=['GET'])
def getUserFeatureByUserId():
    """
    get endpoint
    ---
    tags:
      - userFeatureController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - userId
          properties:
            userId:
              type: string
              description: The user's id.
    responses:
      200:
        description: The response from user_feature_controller
        schema:
    """
    userId = request.json['userId']
    userFeatures = userFeatureRep.findByUserId(userId)
    return json_util.dumps({'userFeatures': userFeatures}), status.HTTP_200_OK, ContentType.json


# def removeUserFeatureById(id: str):
#     userFeatureRep.removeById(id=id)
#     return id
