from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.tracking_rep as trackingRep
import service.face_service as faceService
from agent import id_generator as ig
from agent import time_generator as tg
from domain.tracking import Tracking

mod = Blueprint('tracking_controller', __name__, url_prefix='/trackingController')


@mod.route('/tracking/feature/v1', methods=['POST'])
def trackingByFeature():
    """
    post endpoint
    ---
    tags:
      - trackingController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - subjectId
            - feature
          properties:
            subjectId:
              type: string
              description: The subject's id.
            feature:
              type: array
              default: []
              items:
                type: number
              description: face features
    responses:
      200:
        description: The response from tracking_controller
        schema:
    """
    feature = request.json['feature']
    subjectId = request.json['subjectId']
    deviceMacAddress = request.json['deviceMacAddress']
    # 辨識拿到userId
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    if userId is "":
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    tracking = Tracking(id=ig.generateId('tracking'), userId=userId,subjectId=subjectId,
                        createTime=tg.getNowAsMilli(), deviceMacAddress=deviceMacAddress)
    trackingRep.save(tracking)
    return json_util.dumps({'tracking': tracking.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/tracking/faceImage/v1', methods=['POST'])
def trackingByFaceImage():
    """
    post endpoint
    ---
    tags:
      - trackingController
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
      - name: image
        in: form
        required: true
        type: file
    responses:
      200:
        description: The response from tracking_controller
        schema:
    """
    faceImage = request.files['faceImage'].read()
    subjectId = request.json['subjectId']
    deviceMacAddress = request.json['deviceMacAddress']
    # 先抓出faceFeature...
    feature = faceService._encodingFaceFeature(faceImage)
    if feature is "":
        return 'This picture has multiple/no face', status.HTTP_404_NOT_FOUND
    # 辨識拿到userId...
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    if userId is "":
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    tracking = Tracking(id=ig.generateId('tracking'), userId=userId,subjectId=subjectId,
                        createTime=tg.getNowAsMilli(), deviceMacAddress=deviceMacAddress)
    trackingRep.save(tracking)
    return json_util.dumps({'tracking': tracking.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/trackingLog', methods=['GET'])
def getTrackingBySubjectId():
    subjectId = request.json['subjectId']
    trackings = trackingRep.findBySubjectId(subjectId)
    return json_util.dumps({'trackings': trackings}), status.HTTP_200_OK, ContentType.json
