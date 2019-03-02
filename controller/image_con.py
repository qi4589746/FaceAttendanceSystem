from flask import Blueprint, request
from flask_api import status

import agent.content_type as ContentType
import repository.image_rep as imageRep

mod = Blueprint('image_controller', __name__, url_prefix='/imageController')


@mod.route('image', methods=['GET'])
def getImageByFileId():
    """
    get endpoint
    ---
    tags:
      - imageController
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - fileId
          properties:
            fileId:
              type: string
              description: The image's id.
    responses:
      200:
        description: The image get from the database
        schema:
    """
    fileId = request.json['fileId']
    imageType = fileId.split('.')[1]
    return imageRep.findByFileId(fileId), status.HTTP_200_OK, ContentType.mimeType(imageType)
