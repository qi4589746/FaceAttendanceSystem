import base64
import io
import json

from PIL import Image
from flask import Blueprint

import repository.subject_user_rep as subjectUserRep
import repository.user_rep as userRep
import service.face_service as faceService
from agent import id_generator as ig
from agent import time_generator as tg
from domain.subject_user import SubjectUser
from domain.user import User

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
    featureLimit = 5
    message = socket.receive()
    message = eval(message)
    print(message)
    print(type(message))
    try:
        userName = message['name']
        print(userName)
        description = message['description']
        print(description)
        # subjectId = message['subjectId']
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
            socket.send(str(Message(0, 'OK').__dict__))
            while not socket.closed:
                try:
                    message = socket.receive()
                    data = message.split(',')[1]
                    image = stringToImage(data)
                    print(type(image))
                    print(image.shape)
                    socket.send(str(image.shape))
                except Exception as e:
                    socket.send(str(e))
                    print(e)
            return
    except Exception as e:
        print(str(e))
        socket.send(str(Message(1, 'Error Input, userName and userDescription cannot be empty!').__dict__))


# ws://127.0.0.1:5000/videoStream/recognition_demo
@videoStream.route('/recognition_demo')
def recognitionUser_demo(socket):
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
                faceContent = FaceContent(id="id", name='name', x=x, y=y, h=h, w=w, description="description")
                userList.append(faceContent)
            # print(json.dumps(userList, cls=FaceContentJSONEncoder))
            socket.send(json.dumps(userList, cls=FaceContentJSONEncoder))
        except Exception as e:
            socket.send(str(e))
            print(e)


def stringToImage(base64_string):
    imgData = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgData))
