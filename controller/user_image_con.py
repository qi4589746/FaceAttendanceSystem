from flask import Blueprint, request
from agent import id_generator as ig
from agent import time_generator as tg
from flask_api import status
from bson import json_util
from domain.user_image import UserImage
import repository.user_image_rep as userImageRep
import repository.image_rep as imageRep
import repository.user_rep as userRep
import agent.content_type as ContentType
import face_recognition
import cv2
import controller.user_feature_con as userFeatureController
import _thread

mod = Blueprint('user_image_controller', __name__, url_prefix='/userImageController')


@mod.route('/userImage', methods=['POST'])
def postUserImage():
    """
    post endpoint
    ---
    tags:
      - userImageController
    parameters:
      - userId: body
        in: body
        required: true
        schema:
          id: Product
          required:
            - name
          properties:
            name:
              type: string
              description: The product's name.
    responses:
      200:
        description: The product inserted in the database
        schema:
          $ref: '#/definitions/Product'
    """
    userId = request.json['userId']
    image = request.json['image']
    if userId is None or image is None:
        return '', status.HTTP_400_BAD_REQUEST
    if userRep.findById(userId) is None:
        return '', status.HTTP_404_NOT_FOUND
    if detectFaceAndUpdateDatabase(image) is False:
        return 'This picture has multiple/no face', status.HTTP_400_BAD_REQUEST
    imageId = ig.generateId('faceImage')
    imageRep.save(imageId, image)
    userImage = UserImage(id=userId, imageId=imageId, createTime=tg.getNowAsMilli())
    userImage = userImageRep.save(userImage)
    try:
        _thread.start_new_thread(encodingFaceAndUpdateDatabase, (userId, imageId, image))
    except:
        pass
    return json_util.dumps({'userImage': userImage.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/userImage', methods=['GET'])
def getUserImageByUserId():
    """
    post endpoint
    ---
    tags:
      - products2
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Product
          required:
            - name
          properties:
            name:
              type: string
              description: The product's name.
              default: "Guarana"
    responses:
      200:
        description: The product inserted in the database
        schema:
          $ref: '#/definitions/Product'
    """
    userId = request.json['userId']
    if userRep.findById(userId) is None:
        return '', status.HTTP_404_NOT_FOUND
    userImages = userImageRep.findByUserId(userId)
    return json_util.dumps({'userImages': userImages}), status.HTTP_200_OK, ContentType.json


@mod.route('/userImage', methods=['DELETE'])
def removeUserImageById():
    userImageId = request.json['userImageId']
    userImage = userImageRep.findById(userImageId)
    imageRep.removeById(userImage.imageId)  # remove file
    userImageRep.removeById(userImageId)
    return userImageId, status.HTTP_200_OK


def detectFaceAndUpdateDatabase(image, resize_rate: float = 0.5):
    image = cv2.resize(image, (0, 0), fx=resize_rate, fy=resize_rate)
    rgb_small_frame = image[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    faceNum = len(face_locations)
    if faceNum is not 1:
        return False
    else:
        return True


def encodingFaceAndUpdateDatabase(userId, imageId, image, resize_rate: float = 0.5):
    image = cv2.resize(image, (0, 0), fx=resize_rate, fy=resize_rate)
    rgb_small_frame = image[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    for face_encoding in face_encodings:
        userFeatureController.createUserFeature(userId=userId, imageId=imageId, feature=face_encoding)
    return True
