from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.subject_user_rep as subjectUserRep
import repository.user_feature_rep as userFeatureRep
import repository.user_image_rep as userImageRep
import repository.user_rep as userRep
from agent import id_generator as ig
from agent import time_generator as tg
from domain.user import User

mod = Blueprint('user_controller', __name__, url_prefix='/userController')


@mod.route('/user', methods=['POST'])
def createUser():
    """
    post endpoint
    ---
    tags:
      - userController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - name
          properties:
            userId:
              type: string
              description: The user's id.
              default: ""
            name:
              type: string
              description: The user's name.
    responses:
      200:
        description: The response from user_controller
        schema:
    """
    userId = request.json['userId']
    userName = request.json['name']
    if userName is "":
        return '', status.HTTP_400_BAD_REQUEST
    if userId is '':
        userId = ig.generateId('user')
    else:
        user = userRep.findById(userId)
        if user is not "":
            return '', 226
    user = User(id=userId, name=userName, createTime=tg.getNowAsMilli(), updateTime=tg.getNowAsMilli())
    user = userRep.save(user)
    return json_util.dumps({'user': user.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/user', methods=['GET'])
def getUserById():
    """
    get endpoint
    ---
    tags:
      - userController
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
        description: The response from user_controller
        schema:
    """
    userId = request.json['userId']
    if userId is "":
        return '', status.HTTP_400_BAD_REQUEST
    user = userRep.findById(userId)
    return json_util.dumps({'user': user.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/allUser', methods=['GET'])
def getAllUser():
    """
    get endpoint
    ---
    tags:
      - userController
    responses:
      200:
        description: The response from user_controller
        schema:
    """
    users = userRep.findAll()
    return json_util.dumps({'users': users}), status.HTTP_200_OK, ContentType.json


@mod.route('/user', methods=['DELETE'])
def removeUserByUserId():
    """
    delete endpoint
    ---
    tags:
      - userController
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
        description: The response from user_controller
        schema:
    """
    userId = request.json['userId']
    if userId is "":
        return '', status.HTTP_400_BAD_REQUEST
    userFeatureRep.removeByUserId(userId)
    subjectUserRep.removeByUserId(userId)
    userImageRep.removeByUserId(userId)
    userRep.removeById(userId)
    return userId, status.HTTP_202_ACCEPTED
