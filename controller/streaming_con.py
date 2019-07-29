import urllib.request

import cv2
import numpy as np
from flask import Blueprint, Response

mod = Blueprint('streaming_controller', __name__, url_prefix='/streamingController')


@mod.route('videoStreaming', methods=['GET'])
def getVideoStreamByCameraIP():
    """
    get endpoint
    ---
    tags:
      - streamingController
    parameters:
      - name: cameraIP
        in: form
        require: true
        type: text
    responses:
      200:
        description: The response from streamingController
        schema:
    """
    # cameraIP = request.form['cameraIP']
    cameraIP = 'http://192.168.1.140:5000/video_feed'
    return Response(gen(cameraIP),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(url):
    """Video streaming generator function."""
    bytes = b''
    stream = urllib.request.urlopen(url)
    while True:
        bytes += stream.read(1024)
        # print(bytes)
        # print('------\n')
        a = bytes.find(b'\xff\xd8')  # JPEG start
        b = bytes.find(b'\xff\xd9')  # JPEG end
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]  # actual image
            bytes = bytes[b + 2:]  # other informations

            # decode to colored image ( another option is cv2.IMREAD_GRAYSCALE )
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            # 換成利用agent的camera丟出來
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
