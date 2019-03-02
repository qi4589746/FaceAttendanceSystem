import _thread
import os

import cv2
import face_recognition
from bson import json_util
from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import controller.user_feature_con as userFeatureController
import repository.image_rep as imageRep
import repository.user_feature_rep as userFeatureRep
import repository.user_image_rep as userImageRep
import repository.user_rep as userRep
from agent import id_generator as ig
from agent import time_generator as tg
from app import app
from domain.user_image import UserImage

mod = Blueprint('user_image_controller', __name__, url_prefix='/userImageController')


@mod.route('/userImage', methods=['POST'])
def postUserImage():
    """
    post endpoint
    ---
    tags:
      - userImageController
    parameters:
      - name: userId
        in: form
        required: true
        type: string
      - name: image
        in: file
        required: true
        type: file
    responses:
      200:
        description: The userImage inserted in the database
        schema:
    """
    userId = request.form['userId']
    image = request.files['image']
    imageType = image.content_type
    imageId = ig.generateId('faceImage') + '.' + imageType.split('/')[1]
    print(imageId)
    image.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGE'], imageId))
    image = cv2.imread(app.config['UPLOAD_FOLDER_IMAGE'] + imageId)
    if userId is "" or image is None:
        return json_util.dumps({"message": "empty parameters"}), status.HTTP_400_BAD_REQUEST, ContentType.json
    if userRep.findById(userId) is None:
        return '', status.HTTP_404_NOT_FOUND
    if detectFace(image) is False:
        return 'This picture has multiple/no face', status.HTTP_400_BAD_REQUEST

    with open(app.config['UPLOAD_FOLDER_IMAGE'] + imageId, "rb") as imageFile:
        imageRep.save(imageId, imageFile)
    userImage = UserImage(id=ig.generateId('userImage'), userId=userId, imageId=imageId, createTime=tg.getNowAsMilli(),
                          updateTime=tg.getNowAsMilli())
    userImage = userImageRep.save(userImage)
    _thread.start_new_thread(encodingFaceAndUploadDatabase, (userId, imageId, image))
    return json_util.dumps({'userImage': userImage.__dict__}), status.HTTP_200_OK, ContentType.json

@mod.route('/userImage', methods=['GET'])
def getUserImageByUserId():
    """
    get endpoint
    ---
    tags:
      - userImageController
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
              description: The userImage's userId.
    responses:
      200:
        description: The userImage inserted from the database
        schema:
    """
    userId = request.json['userId']
    if userRep.findById(userId) is None:
        return '', status.HTTP_404_NOT_FOUND
    userImages = userImageRep.findByUserId(userId)
    return json_util.dumps({'userImages': userImages}), status.HTTP_200_OK, ContentType.json


@mod.route('/userImage', methods=['DELETE'])
def removeUserImageById():
    """
        delete endpoint
        ---
        tags:
          - userImageController
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
                description: The userImage's userId.
        responses:
          200:
            description: The userImage deleted from the database
            schema:
        """
    userImageId = request.json['userImageId']
    userImage = userImageRep.findById(userImageId)
    userFeatureRep.removeByImageId(userImage['imageId'])
    imageRep.removeById(userImage['imageId'])  # remove file
    userImageRep.removeById(userImageId)
    return userImageId, status.HTTP_200_OK


def detectFace(image, resize_rate: float = 0.5):
    # print(image)
    # _image = cv2.imdecode(numpy.fromstring(image, numpy.uint8), cv2.IMREAD_COLOR)
    _image = cv2.resize(image, (0, 0), fx=resize_rate, fy=resize_rate)
    rgb_small_frame = _image[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    faceNum = len(face_locations)
    if faceNum is not 1:
        return False
    else:
        return True


# image = cv2.imdecode(numpy.fromstring(image, numpy.uint8), cv2.IMREAD_COLOR)
# cv2.error: OpenCV(4.0.0) /io/opencv/modules/imgcodecs/src/loadsave.cpp:725: error: (-215:Assertion failed) !buf.empty() && buf.isContinuous() in function 'imdecode_'
def encodingFaceAndUploadDatabase(userId, imageId, image, resize_rate: float = 0.5):
    # print(image)
    # _image = cv2.imdecode(numpy.fromstring(image, numpy.uint8), cv2.IMREAD_COLOR)
    _image = cv2.resize(image, (0, 0), fx=resize_rate, fy=resize_rate)
    rgb_small_frame = _image[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    for face_encoding in face_encodings:
        userFeatureController.createUserFeature(userId=userId, imageId=imageId, feature=face_encoding.tolist())
    os.remove(app.config['UPLOAD_FOLDER_IMAGE'] + imageId)
    return True
