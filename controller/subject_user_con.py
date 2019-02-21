from flask import Blueprint, request
from agent import id_generator as ig
from agent import time_generator as tg
from flask_api import status
from bson import json_util
from domain.subject_user import SubjectUser
import repository.subject_user_rep as subjectUserRep
import agent.content_type as ContentType

mod = Blueprint('subject_user_controller', __name__, url_prefix='/subjectUserController')


@mod.route('/subjectUser', methods=['POST'])
def createSubjectUser():
    userId = request.json['userId']
    subjectId = request.json['subjectId']
    subjectUser = subjectUserRep.findBySubjectIdAndUserId(subjectId, userId)
    if subjectUser is not None:
        return json_util.dumps({'subjectUser': subjectUser}), status.HTTP_201_CREATED, ContentType.json
    else:
        subjectUser = SubjectUser(id=ig.generateId('subjectUser'), userId=userId, subjectId=subjectId, createTime=tg.getNowAsMilli())
        subjectUser = subjectUserRep.save(subjectUser)
        return json_util.dumps({'subjectUser': subjectUser}), status.HTTP_200_OK, ContentType.json


@mod.route('/subjectUser', methods=['GET'])
def getSubjectUserBySubjectId():
    subjectId = request.json['subjectId']
    subjectUsers = subjectUserRep.findBySubjectId(subjectId)
    return json_util.dumps({'subjectUsers': subjectUsers}), status.HTTP_200_OK, ContentType.json


@mod.route('/subjectUser', methods=['DELETE'])
def removeSubjectUserBySubjectIdAndUserId():
    userId = request.json['userId']
    subjectId = request.json['subjectId']
    subjectUserRep.removeBySubjectIdAndUserId(subjectId=subjectId, userId=userId)
    return '', status.HTTP_200_OK
