from flask import Blueprint, request
from flask_api import status

from agent import streamingConfiger as streamingCon
from agent.db import mongo
from service import face_service as faceService

mod = Blueprint('streamingConfiger_controller', __name__, url_prefix='/streamingConfigerController')


@mod.route('/matchRate', methods=['POST'])
def setMatchRate():
    matchRate = request.form['matchRate']
    streamingCon.match_rate = float(matchRate)
    return str(streamingCon.match_rate), status.HTTP_200_OK


@mod.route('/matchRate', methods=['GET'])
def getMatchRate():
    return str(streamingCon.match_rate), status.HTTP_200_OK


@mod.route('/sampling', methods=['POST'])
def setSampling():
    sampling = request.form['sampling']
    streamingCon.featureLimit = int(sampling)
    return str(streamingCon.featureLimit), status.HTTP_200_OK


@mod.route('/sampling', methods=['GET'])
def getSampling():
    return str(streamingCon.featureLimit), status.HTTP_200_OK


@mod.route('/destory', methods=['POST'])
def destory():
    mongo.db.user.drop()
    mongo.db.model.drop()
    mongo.db.subjectModel.drop()
    mongo.db.subjectUser.drop()
    mongo.db.userFeature.drop()
    faceService._removeModelBySubjectId('demoSubject')
    return str('Boom'), status.HTTP_200_OK
