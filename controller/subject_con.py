from flask import Blueprint, request
from agent import id_generator as ig
from agent import time_generator as tg
from flask_api import status
from bson import json_util
from domain.subject import Subject
import agent.content_type as ContentType
import repository.subject_rep as subjectRep
import repository.subject_model_rep as subjectModelRep
import repository.subject_user_rep as subjectUserRep
import repository.tracking_rep as trackingRep


mod = Blueprint('subject_controller', __name__, url_prefix='/subjectController')


@mod.route('subject', methods=['POST'])
def createSubject():
    subjectName = request.json['subjectName']
    subjectId = request.json['subjectId']
    if subjectId is None:
        subjectId = ig.generateId('subject')
    subject = Subject(id=subjectId,
                      name=subjectName,
                      createTime=tg.getNowAsMilli(),
                      updateTime=tg.getNowAsMilli())
    subject = subjectRep.save(subject)
    return json_util.dumps({'subject': subject}), status.HTTP_200_OK, ContentType.json


@mod.route('subject', methods=['GET'])
def getSubjectBySubjectId():
    subjectId = request.json['subjectId']
    subject = subjectRep.findById(subjectId)
    return json_util.dumps({'subject': subject}), status.HTTP_200_OK, ContentType.json


@mod.route('subject', methods=['PUT'])
def updateSubject():
    subjectId = request.json['subjectId']
    subjectName = request.json['subjectName']
    subject = subjectRep.findById(subjectId)
    if subject is None:
        return 'Not found', status.HTTP_404_NOT_FOUND
    else:
        subject['name'] = subjectName
        subject = subjectRep.update(subject)
        return json_util.dumps({'subject': subject}), status.HTTP_200_OK, ContentType.json


@mod.route('subject', methods=['DELETE'])
def removeSubjectAndRelationDataBySubjectId():
    subjectId = request.json['subjectId']
    subjectModelRep.removeBySubjectId(subjectId)
    subjectUserRep.removeBySubjectId(subjectId)
    trackingRep.removeBySubjectId(subjectId)
    subjectRep.removeById(subjectId)
    return subjectId, status.HTTP_200_OK

