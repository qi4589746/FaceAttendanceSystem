from flasgger import Swagger
from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)
swag = Swagger(app)
app.config.from_object('config')

# from testapi import mod as testModule
# app.register_blueprint(testModule)

#
from controller.user_con import mod as userModule
app.register_blueprint(userModule)

#
from controller.face_con import mod as faceModule
app.register_blueprint(faceModule)

#
from controller.subject_con import mod as subjectModule
app.register_blueprint(subjectModule)

#
from controller.subject_model_con import mod as subjectModelModule
app.register_blueprint(subjectModelModule)

#
from controller.subject_user_con import mod as subjectUserModule
app.register_blueprint(subjectUserModule)

#
from controller.tracking_con import mod as trackingModule
app.register_blueprint(trackingModule)

#
from controller.user_feature_con import mod as userFeatureModule
app.register_blueprint(userFeatureModule)

#
from controller.user_image_con import mod as userImageModule
app.register_blueprint(userImageModule)

#
from controller.image_con import mod as imageModule
app.register_blueprint(imageModule)

#
import service.face_service as faceService
faceService._updateAllModel()

#
import service.demo_service as demoService

demoService._initializationDatabase()

#
from controller.videoSocket_con import videoStream

sockets.register_blueprint(videoStream)

#
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
server.serve_forever()

# if __name__ == "__main__":
#     from gevent import pywsgi
#     from geventwebsocket.handler import WebSocketHandler
#
#     server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
#     server.serve_forever()
