from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.model_rep as modelRep
import repository.subject_model_rep as subjectModelRep
import repository.subject_user_rep as subjectUserRep
import repository.user_feature_rep as userFeatureRep
from agent import id_generator as ig
from agent import time_generator as tg
from domain.model import Model
from domain.subject_model import SubjectModel

mod = Blueprint('subject_model_controller', __name__, url_prefix='/subjectModelController')


@mod.route('/subjectModel', methods=['GET'])
def getSubjectModel():
    """
    delete endpoint
    ---
    tags:
      - subjectModelController
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
        description: The response from subject_model_controller
        schema:
    """
    subjectId = request.json['subjectId']
    subjectModel = subjectModelRep.findBySubjectId(subjectId)
    model = modelRep.findById(subjectModel['modelId'])
    return json_util.dumps({'model': model}), status.HTTP_200_OK, ContentType.json


@mod.route('/subjectModel', methods=['POST'])
def updateSubjectModel():
    """
    post endpoint
    ---
    tags:
      - subjectModelController
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
        description: The response from subject_model_controller
        schema:
    """
    subjectId = request.json['subjectId']
    users = subjectUserRep.findBySubjectId(subjectId)
    print(users)
    userIds = []
    modelUsers = []
    modelFeature = []
    for user in users:
        userIds.append(user['userId'])
    for userId in userIds:
        userFeatures = userFeatureRep.findByUserId(userId)
        for userFeature in userFeatures:
            modelUsers.append(userId)
            modelFeature.append(userFeature['feature'])
    model = Model(id=ig.generateId('model'), userIds=modelUsers, encodings=modelFeature, createTime=tg.getNowAsMilli(),
                  updateTime=tg.getNowAsMilli())
    print(model)
    createAndUpdateSubjectModel(subjectId=subjectId, model=model)
    return subjectId, status.HTTP_200_OK


def createAndUpdateSubjectModel(subjectId: str, model):
    currentModel = subjectModelRep.findBySubjectId(subjectId)
    if currentModel is None:
        modelRep.save(model)
        currentModel = SubjectModel(id=ig.generateId('subjectModel'), subjectId=subjectId,
                                    modelId=model.id, createTime=tg.getNowAsMilli(),
                                    updateTime=tg.getNowAsMilli())
        currentModel = subjectModelRep.save(currentModel)
    else:
        previousModelId = currentModel['modelId']
        modelRep.removeById(previousModelId)
        currentModel['modelId'] = model.id
        modelRep.save(model)
        currentModel = subjectModelRep.update(currentModel)
    return currentModel


def removeSubjectModel(subjectId: str):
    currentModel = subjectModelRep.findBySubjectId(subjectId)
    if currentModel is None:
        return subjectId
    else:
        modelId = currentModel['modelId']
        modelRep.removeById(modelId)
        subjectModelRep.removeById(subjectId)
        return subjectId
