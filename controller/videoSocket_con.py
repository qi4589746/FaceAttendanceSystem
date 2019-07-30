import base64

import cv2
import numpy as np
from flask import Blueprint

videoStream = Blueprint(r'videoStream', __name__, url_prefix=r'/videoStream')


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
            print("======================")
        except Exception as e:
            socket.send(str(e))
            print(e)


def readb64(base64_string):
    imgData = base64.b64decode(base64_string)
    nparr = np.fromstring(imgData, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image
