from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.subject_user_rep as subjectUserRep
from agent import id_generator as ig
from agent import time_generator as tg
from domain.subject_user import SubjectUser

mod = Blueprint('subject_user_controller', __name__, url_prefix='/subjectUserController')


@mod.route('/subjectUser', methods=['POST'])
def createSubjectUser():
    """
    post endpoint
    ---
    tags:
      - subjectUserController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - userId
            - subjectId
          properties:
            subjectId:
              type: string
              description: The subject's id.
            userId:
              type: string
              description: The user's id.
    responses:
      200:
        description: The response from subject_user_controller
        schema:
    """
    userId = request.json['userId']
    subjectId = request.json['subjectId']
    subjectUser = subjectUserRep.findBySubjectIdAndUserId(subjectId, userId)
    if subjectUser is not None:
        return json_util.dumps({'subjectUser': subjectUser}), status.HTTP_201_CREATED, ContentType.json
    else:
        subjectUser = SubjectUser(id=ig.generateId('subjectUser'), userId=userId, subjectId=subjectId,
                                  createTime=tg.getNowAsMilli(), updateTime=tg.getNowAsMilli())
        subjectUser = subjectUserRep.save(subjectUser)
        return json_util.dumps({'subjectUser': subjectUser.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/subjectUser', methods=['GET'])
def getSubjectUserBySubjectId():
    """
    get endpoint
    ---
    tags:
      - subjectUserController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - subjectId
          properties:
            subjectId:
              type: string
              description: The subject's id.
            userId:
              type: string
              description: The user's id.
    responses:
      200:
        description: The response from subject_user_controller
        schema:
    """
    subjectId = request.json['subjectId']
    subjectUsers = subjectUserRep.findBySubjectId(subjectId)
    return json_util.dumps({'subjectUsers': subjectUsers}), status.HTTP_200_OK, ContentType.json


@mod.route('/subjectUser', methods=['DELETE'])
def removeSubjectUserBySubjectIdAndUserId():
    """
    get endpoint
    ---
    tags:
      - subjectUserController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - userId
            - subjectId
          properties:
            subjectId:
              type: string
              description: The subject's id.
    responses:
      200:
        description: The response from subject_user_controller
        schema:
    """
    userId = request.json['userId']
    subjectId = request.json['subjectId']
    subjectUserRep.removeBySubjectIdAndUserId(subjectId=subjectId, userId=userId)
    return '', status.HTTP_200_OK
