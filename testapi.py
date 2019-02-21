from flask import Blueprint, request
from agent.db import mongo
from domain.user import User
from agent import id_generator as ig
from agent import time_generator as tg
from bson import json_util
from flask_api import status
import repository.user_rep as usp
import agent.content_type as ContentType


mod = Blueprint('test', __name__, url_prefix='/test')


@mod.route('/user', methods=['POST'])
def test1():
    user = User(id=ig.generateId("user"), name="test1", createTime=tg.getNowAsMilli(), updateTime=tg.getNowAsMilli())
    user = usp.save(user)
    return json_util.dumps({'user': user.__dict__}), status.HTTP_200_OK, ContentType.json


@mod.route('/userMul', methods=['GET'])
def test4():
    id = request.json['id']
    name = request.json['name']
    user = usp.testFind(id=id, name=name)
    return json_util.dumps({'user': user}), status.HTTP_200_OK, ContentType.json

@mod.route('/user', methods=['GET'])
def test2():
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
    users = [ doc for doc in mongo.db.user.find()]
    print(users)
    return json_util.dumps({'users': users}), status.HTTP_200_OK, ContentType.json


@mod.route('/userById', methods=['GET'])
def test3():
    """
    post endpoint
    ---
    tags:
      - products
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
    user = usp.findById(userId)
    print(user)
    print(type(user))
    user['name'] = '1234'
    user = usp.update(user)
    # return "OK"
    return json_util.dumps({'user': user}), status.HTTP_200_OK, ContentType.json
