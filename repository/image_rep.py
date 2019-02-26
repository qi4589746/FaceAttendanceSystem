from agent.db import mongo


def save(fileId: str, file):
    mongo.save_file(fileId, file, base="faceImage")
    return


def save(fileId: str, file):
    mongo.save_file(fileId, file, base="faceImage")
    return


def findByFileId(fileId: str):
    return mongo.send_file(fileId, base="faceImage")


def get_idByFileId(fileId: str):
    import gridfs
    fs = gridfs.GridFS(mongo.db, collection="faceImage")
    return fs.find_one({"filename": fileId})._file['_id']


def removeById(fileId: str):
    """
    implement the method
    """
    import gridfs
    fs = gridfs.GridFS(mongo.db, collection="faceImage")
    fs.delete(get_idByFileId(fileId))
    pass
