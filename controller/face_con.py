import time

from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.user_rep as userRep
import service.face_service as faceService

mod = Blueprint('face_controller', __name__, url_prefix='/faceController')


@mod.route('/recognition/feature', methods=['PUT'])
def recognitionByFeature():
    """
    put endpoint
    ---
    tags:
      - faceController
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
        description: The response from recognition service
        schema:
    """
    feature = request.json['feature']
    subjectId = request.json['subjectId']
    # 辨識拿到userId
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    if userId is "":
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    else:
        user = userRep.findById(userId)
        return json_util.dumps({'user': user}), status.HTTP_200_OK, ContentType.json


@mod.route('/recognition/faceImage', methods=['PUT'])
def recognitionByFaceImage():
    """
    put endpoint
    ---
    tags:
      - faceController
    parameters:
      - name: subjectId
        in: form
        require: true
        type: text
      - name: faceImage
        in: form
        require: true
        type: file
    responses:
      200:
        description: The response from recognition service
        schema:
    """
    tStart = time.time()
    faceImage = request.files['faceImage']
    subjectId = request.form['subjectId']
    # 先抓出faceFeature...
    feature = faceService._encodingFaceFeature(faceImage)
    if feature is None:
        return 'This picture has multiple/no face', status.HTTP_404_NOT_FOUND
    # 辨識拿到userId...
    userId = faceService._recognizeByFeatureAndSubjectId(subjectId=subjectId, feature=feature)
    tEnd = time.time()
    print(tEnd - tStart)
    if userId is "":
        return 'not found this people in the subject', status.HTTP_404_NOT_FOUND
    else:
        user = userRep.findById(userId)
        return json_util.dumps({'user': user}), status.HTTP_200_OK, ContentType.json
