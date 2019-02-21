from flask import Flask
from flasgger import Swagger


app = Flask(__name__)
app.config.from_object('config')

from testapi import mod as testModule
app.register_blueprint(testModule)

from controller.user_con import mod as userModule
app.register_blueprint(userModule)

from controller.face_controller import mod as faceModule
app.register_blueprint(faceModule)

from controller.subject_con import mod as subjectModule
app.register_blueprint(subjectModule)

from controller.subject_model_con import mod as subjectModelModule
app.register_blueprint(subjectModelModule)

from controller.subject_user_con import mod as subjectUserModule
app.register_blueprint(subjectUserModule)

from controller.tracking_con import mod as trackingModule
app.register_blueprint(trackingModule)

from controller.user_feature_con import mod as suerFeatureModule
app.register_blueprint(suerFeatureModule)

from controller.user_image_con import mod as userImageModule
app.register_blueprint(userImageModule)

swag = Swagger(app)
# app.run(debug=True)