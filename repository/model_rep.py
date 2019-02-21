from agent.db import mongo


def save(fileId: str, file):
    mongo.save_file(fileId, file, base="model")


def findByFileId(fileId: str):
    return mongo.send_file(fileId, base="model")


def removeById(fileId: str):
    """
    implement the method
    """
    pass
