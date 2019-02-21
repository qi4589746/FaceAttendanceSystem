from flask import Blueprint, request
from flask_api import status
from bson import json_util
import repository.user_rep as userRep
import agent.content_type as ContentType
import service.face_service as faceService


mod = Blueprint('face_controller', __name__, url_prefix='/face_controller')


@mod.route('/recognition/feature', methods=['PUT'])
def recognitionByFeature():
    feature = request.json['feature']
    subjectId = request.json['subjectId']
    # 辨識拿到userId
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    if userId is None:
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    else:
        user = userRep.findById(userId)
        return json_util.dumps({'user': user}), status.HTTP_200_OK, ContentType.json


@mod.route('/recognition/faceImage', methods=['PUT'])
def recognitionByFaceImage():
    faceImage = request.json['faceImage']
    subjectId = request.json['subjectId']
    # 先抓出faceFeature...
    feature = faceService._encodingFaceFeature(faceImage)
    if feature is None:
        return 'This picture has multiple/no face', status.HTTP_404_NOT_FOUND
    # 辨識拿到userId...
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    if userId is None:
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    else:
        user = userRep.findById(userId)
        return json_util.dumps({'user': user}), status.HTTP_200_OK, ContentType.json
