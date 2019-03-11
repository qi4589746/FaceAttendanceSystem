from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.subject_model_rep as subjectModelRep
import repository.subject_rep as subjectRep
import repository.subject_user_rep as subjectUserRep
import repository.tracking_rep as trackingRep
from agent import id_generator as ig
from agent import time_generator as tg
from domain.subject import Subject

mod = Blueprint('subject_controller', __name__, url_prefix='/subjectController')


@mod.route('/subject', methods=['POST'])
def createSubject():
    """
    post endpoint
    ---
    tags:
      - subjectController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - subjectName
          properties:
            subjectName:
              type: string
              description: The subject's name.
            subjectId:
              type: string
              description: The subject's id.
              default: ""
    responses:
      200:
        description: The response from subject_controller
        schema:
    """
    subjectName = request.json['subjectName']
    subjectId = request.json['subjectId']

    if subjectId is "":
        subjectId = ig.generateId('subject')
    else:
        subject = subjectRep.findById(subjectId)
        print(subject)
        if subject is not None:
            return '', 226

    subject = Subject(id=subjectId,
                      name=subjectName,
                      createTime=tg.getNowAsMilli(),
                      updateTime=tg.getNowAsMilli())
    subject = subjectRep.save(subject)
    return json_util.dumps({'subject': subject.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/subject', methods=['GET'])
def getSubjectBySubjectId():
    """
    get endpoint
    ---
    tags:
      - subjectController
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
    responses:
      200:
        description: The response from subject_controller
        schema:
    """
    subjectId = request.json['subjectId']
    subject = subjectRep.findById(subjectId)
    return json_util.dumps({'subject': subject}), status.HTTP_200_OK, ContentType.json


@mod.route('/subject', methods=['PUT'])
def updateSubject():
    """
    put endpoint
    ---
    tags:
      - subjectController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - subjectId
            - subjectName
          properties:
            subjectName:
              type: string
              description: The subject's name.
            subjectId:
              type: string
              description: The subject's id.
    responses:
      200:
        description: The response from subject_controller
        schema:
    """
    subjectId = request.json['subjectId']
    subjectName = request.json['subjectName']
    subject = subjectRep.findById(subjectId)
    if subject is None:
        return 'Not found', status.HTTP_404_NOT_FOUND
    else:
        subject['name'] = subjectName
        subject = subjectRep.update(subject)
        return json_util.dumps({'subject': subject}), status.HTTP_200_OK, ContentType.json


@mod.route('/subject', methods=['DELETE'])
def removeSubjectAndRelationDataBySubjectId():
    """
    delete endpoint
    ---
    tags:
      - subjectController
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
    responses:
      200:
        description: The response from subject_controller
        schema:
    """
    subjectId = request.json['subjectId']
    subjectModelRep.removeBySubjectId(subjectId)
    subjectUserRep.removeBySubjectId(subjectId)
    trackingRep.removeBySubjectId(subjectId)
    subjectRep.removeById(subjectId)
    return subjectId, status.HTTP_200_OK

