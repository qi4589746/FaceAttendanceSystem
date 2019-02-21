from flask import Blueprint, request
from agent import id_generator as ig
from agent import time_generator as tg
from flask_api import status
from bson import json_util
from domain.tracking import Tracking
import repository.tracking_rep as trackingRep
import agent.content_type as ContentType
import service.face_service as faceService

mod = Blueprint('tracking_controller', __name__, url_prefix='/trackingController')


@mod.route('tracking/feature/v1', methods=['POST'])
def trackingByFeature():
    feature = request.json['feature']
    subjectId = request.json['subjectId']
    deviceMacAddress = request.json['deviceMacAddress']
    # 辨識拿到userId
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    if userId is None:
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    tracking = Tracking(id=ig.generateId('tracking'), userId=userId,subjectId=subjectId,
                        createTime=tg.getNowAsMilli(), deviceMacAddress=deviceMacAddress)
    trackingRep.save(tracking)
    return json_util.dumps({'tracking': tracking.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('tracking/faceImage/v1', methods=['POST'])
def trackingByFaceImage():
    faceImage = request.json['faceImage']
    subjectId = request.json['subjectId']
    deviceMacAddress = request.json['deviceMacAddress']
    # 先抓出faceFeature...
    feature = faceService._encodingFaceFeature(faceImage)
    if feature is None:
        return 'This picture has multiple/no face', status.HTTP_404_NOT_FOUND
    # 辨識拿到userId...
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    if userId is None:
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    tracking = Tracking(id=ig.generateId('tracking'), userId=userId,subjectId=subjectId,
                        createTime=tg.getNowAsMilli(), deviceMacAddress=deviceMacAddress)
    trackingRep.save(tracking)
    return json_util.dumps({'tracking': tracking.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('trackingLog', methods=['GET'])
def getTrackingBySubjectId():
    subjectId = request.json['subjectId']
    trackings = trackingRep.findBySubjectId(subjectId)
    return json_util.dumps({'trackings': trackings}), status.HTTP_200_OK, ContentType.json
