import pickle

import cv2
import face_recognition
import numpy

import repository.model_rep as modelRep
import repository.subject_model_rep as subjectModelRep

_subjectModels = {}


def _updateAllModel():
    for subjectModel in subjectModelRep.findAll():
        model = modelRep.findByFileId(subjectModel['modelId'])
        # model 須做處理，轉成辨識的使用資料型態，現在為file
        model = pickle.load(model)
        _subjectModels.update({subjectModel['subjectId']: model})


def _updateModelBySubjectId(subjectId: str):
    subjectModel = subjectModelRep.findBySubjectId(subjectId)
    model = modelRep.findByFileId(subjectModel['modelId'])
    model = pickle.load(model)
    _subjectModels.update({subjectModel.subjectId: model})


def _removeModelBySubjectId(subjectId: str):
    del _subjectModels[subjectId]


def _recognizeByImageAndSubjectId(subjectId: str, image, match_rate: float = 0.5, resize_rate: float = 0.5):
    image = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_COLOR)
    model = _subjectModels[subjectId]
    small_frame = cv2.resize(image, (0, 0), fx=resize_rate, fy=resize_rate)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    faceNum = len(face_locations)
    if faceNum < 1:
        return 0
    elif faceNum > 1:
        return 1
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(model['encodings'], face_encoding, tolerance=match_rate)
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                userId = model['userIds'][i]
                counts[userId] = counts.get(userId, 0) + 1
            userId = max(counts, key=counts.get)
    return userId


def _recognizeByFeatureAndSubjectId(subjectId: str, feature, match_rate: float = 0.5):

    model = _subjectModels[subjectId]
    if len(feature) is not 128:
        return ""
    matches = face_recognition.compare_faces(model['encodings'], feature, tolerance=match_rate)
    if True in matches:
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}
        for i in matchedIdxs:
            userId = model['userIds'][i]
            counts[userId] = counts.get(userId, 0) + 1
        userId = max(counts, key=counts.get)
    return userId


def _encodingFaceFeature(image, resize_rate: float = 0.5):
    image = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_COLOR)
    small_frame = cv2.resize(image, (0, 0), fx=resize_rate, fy=resize_rate)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    faceNum = len(face_locations)
    if faceNum is not 1:
        return None
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    for face_encoding in face_encodings:
        return face_encoding


def _hasOnlyOneFace(image, resize_rate: float = 0.5):
    image = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(image, (0, 0), fx=resize_rate, fy=resize_rate)
    rgb_small_frame = image[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    faceNum = len(face_locations)
    if faceNum is not 1:
        return False
    else:
        return True
