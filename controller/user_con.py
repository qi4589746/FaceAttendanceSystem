from flask import Blueprint, request
from agent import id_generator as ig
from agent import time_generator as tg
from flask_api import status
from bson import json_util
from domain.user import User
import repository.user_rep as userRep
import agent.content_type as ContentType
import repository.user_feature_rep as userFeatureRep
import repository.subject_user_rep as subjectUserRep
import repository.user_image_rep as userImageRep

mod = Blueprint('user_controller', __name__, url_prefix='/userController')


@mod.route('/user', methods=['POST'])
def createUser():
    userId = request.json['userId']
    userName = request.json['name']
    if userName is None:
        return '', status.HTTP_400_BAD_REQUEST
    if userId is '':
        userId = ig.generateId('user')
    else:
        user = userRep.findById(userId)
        if user is not None:
            return '', 226
    user = User(id=userId, name=userName, createTime=tg.getNowAsMilli())
    user = userRep.save(user)
    return json_util.dumps({'user': user.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/user', methods=['GET'])
def getUserById():
    userId = request.json['userId']
    if userId is None:
        return '', status.HTTP_400_BAD_REQUEST
    user = userRep.findById(userId)
    return json_util.dumps({'user': user.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/allUser', methods=['GET'])
def getAllUser():
    users = userRep.findAll()
    return json_util.dumps({'users': users}), status.HTTP_200_OK, ContentType.json


@mod.route('/user', methods=['DELETE'])
def removeUserByUserId():
    userId = request.json['userId']
    if userId is None:
        return '', status.HTTP_400_BAD_REQUEST
    userFeatureRep.removeByUserId(userId)
    subjectUserRep.removeByUserId(userId)
    userImageRep.removeByUserId(userId)
    userRep.removeById(userId)
    return userId, status.HTTP_202_ACCEPTED
