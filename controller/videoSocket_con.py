import base64

import cv2
import numpy as np
from flask import Blueprint

videoStream = Blueprint(r'videoStream', __name__, url_prefix=r'/videoStream')


class Message:
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


@videoStream.route('/register')
def registerUser(socket):
    message = socket.receive()
    try:
        userName = message['name']
        userDescription = message['userDescription']
        if ~(len(userDescription) > 0) or ~(len(userName) > 0):
            message = Message(1, 'userName and userDescription cannot be empty!')
            socket.send(message.__dict__)
            return
        else:
            return
    except Exception as e:
        socket.send('Error Input')


@videoStream.route('/upload')
def echo_socket(socket):
    while not socket.closed:
        try:
            message = socket.receive()
            data = message.split(',')[1]
            image = readb64(data)
            print(type(image))
            print(image.shape)
            # cv2.imshow('.123', image)
            # cv2.imwrite('output.jpg', image)
            socket.send(str(image.shape))
        except Exception as e:
            socket.send(str(e))
            print(e)


def readb64(base64_string):
    imgData = base64.b64decode(base64_string)
    nparr = np.fromstring(imgData, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image
