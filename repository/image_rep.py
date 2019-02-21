from agent.db import mongo


def save(fileId: str, file):
    mongo.save_file(fileId, file, base="faceImage")


def findByFileId(fileId: str):
    return mongo.send_file(fileId, base="faceImage")


def removeById(fileId: str):
    """
    implement the method
    """
    pass
