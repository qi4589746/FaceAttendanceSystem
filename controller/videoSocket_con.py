import base64
import io
import json

import geventwebsocket
from PIL import Image
from flask import Blueprint

import repository.model_rep as modelRep
import repository.subject_model_rep as subjectModelRep
import repository.subject_user_rep as subjectUserRep
import repository.user_feature_rep as userFeatureRep
import repository.user_rep as userRep
import service.face_service as FaceService
import service.face_service as faceService
from agent import id_generator as ig
from agent import streamingConfiger as streamingCon
from agent import time_generator as tg
from domain.model import Model
from domain.subject_model import SubjectModel
from domain.subject_user import SubjectUser
from domain.user import User
from domain.user_feature import UserFeature

videoStream = Blueprint(r'videoStream', __name__, url_prefix=r'/videoStream')


class Message:
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


class FaceContent:
    def __init__(self, name: str, id: str, x: float, y: float, h: float, w: float, description: str):
        self.name = name
        self.id = id
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.description = description

    def __jsonencode__(self):
        return {'id': self.id,
                'name': self.name,
                'x': self.x,
                'y': self.y,
                'h': self.h,
                'w': self.w,
                'description': self.description}


class FaceContentJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__jsonencode__'):
            return obj.__jsonencode__()
        return json.JSONEncoder.default(self, obj)


# ws://127.0.0.1:5000/videoStream/register_demo
@videoStream.route('/register_demo')
def registerUser_demo(socket):
    userList = []
    counter = 0
    waitFrame = streamingCon.waitFrame
    featureLimit = streamingCon.featureLimit
    message = socket.receive()
    message = eval(message)
    try:
        userName = message['name']
        description = message['description']
        subjectId = 'demoSubject'
        if not (len(description) > 0) or not (len(userName) > 0):
            socket.send(str(Message(1, 'userName and description cannot be empty!').__dict__))
            return
        else:
            user = User(id=ig.generateId('user'), name=userName, description=description,
                        createTime=tg.getNowAsMilli(), updateTime=tg.getNowAsMilli())
            userRep.save(user)
            subjectUser = SubjectUser(id=ig.generateId('subjectUser'), userId=user.id, subjectId=subjectId,
                                      createTime=tg.getNowAsMilli(), updateTime=tg.getNowAsMilli(), role=2)
            subjectUserRep.save(subjectUser)
            # print(str(Message(0, 'OK').__dict__))
            socket.send(str(Message(0, 'OK').__dict__))
            theFirst = True
            registerFeature = []
            while not socket.closed:
                try:
                    message = socket.receive()
                    data = message.split(',')[1]
                    image = stringToImage(data)
                    facesData = faceService._getFacesData(image)
                    if len(facesData) == 1:
                        if theFirst:
                            registerFeature.append(facesData[0][1])
                            featureLimit -= 1
                            theFirst = False
                        counter += 1
                        if counter == waitFrame:
                            counter = 0
                            if faceService._compareFeature(registerFeature[0], facesData[0][1]) < (
                                    streamingCon.match_rate + 0.1):
                                registerFeature.append(facesData[0][1])
                                featureLimit -= 1
                        if featureLimit == 0:
                            for faceFeature in registerFeature:
                                userFeature = UserFeature(id=ig.generateId('userFeature'), userId=user.id,
                                                          imageId="systemCreated", createTime=tg.getNowAsMilli(),
                                                          feature=faceFeature.tolist(), updateTime=tg.getNowAsMilli())
                                userFeatureRep.save(userFeature)
                                updateSubjectModel(subjectId)
                            socket.send(str(Message(0, 'Completed').__dict__))
                            break
                    else:
                        socket.send(str(Message(1, 'There is not only one person!').__dict__))
                except Exception as e:
                    try:
                        socket.send(str(e))
                        print(e)
                    except geventwebsocket.exceptions.WebSocketError as e:
                        print(e)
            return
    except Exception as e:
        try:
            print(str(e))
            socket.send(str(Message(1, 'Error Input, userName and userDescription cannot be empty!').__dict__))
        except geventwebsocket.exceptions.WebSocketError as e:
            print(e)
    except geventwebsocket.exceptions.WebSocketError as e:
        print(e)


# ws://127.0.0.1:5000/videoStream/recognition_demo
@videoStream.route('/recognition_demo')
def recognitionUser_demo(socket):
    subjectId = 'demoSubject'
    socket.send(str(Message(0, 'OK').__dict__))
    while not socket.closed:
        userList = []
        try:
            message = socket.receive()
            data = message.split(',')[1]
            image = stringToImage(data)
            facesData = faceService._getFacesData(image)
            for faceData in facesData:
                (top, right, bottom, left) = faceData[0]
                x = left
                y = top
                h = bottom - top
                w = right - left
                userId = faceService._recognizeByFeatureAndSubjectId(feature=faceData[1], subjectId=subjectId,
                                                                     match_rate=streamingCon.match_rate)
                if userId is not None:
                    user = userRep.findById(userId)
                    faceContent = FaceContent(id=user['id'], name=user['name'], x=x, y=y, h=h, w=w,
                                              description=user['description'])
                    userList.append(faceContent)
                else:
                    faceContent = FaceContent(id='Unknown', name='Unknown', x=x, y=y, h=h, w=w,
                                              description='Unknown')
                    userList.append(faceContent)
            # print(json.dumps(userList, cls=FaceContentJSONEncoder))
            socket.send(json.dumps(userList, cls=FaceContentJSONEncoder))
        except geventwebsocket.exceptions.WebSocketError as e:
            print(e)
        except Exception as e:
            try:
                socket.send(str(e))
                print(e)
            except geventwebsocket.exceptions.WebSocketError:
                print(e)


def stringToImage(base64_string):
    imgData = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgData))


def updateSubjectModel(subjectId):
    users = subjectUserRep.findBySubjectId(subjectId)
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
    createAndUpdateSubjectModel(subjectId=subjectId, model=model)
    FaceService._updateModelBySubjectId(subjectId)


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
