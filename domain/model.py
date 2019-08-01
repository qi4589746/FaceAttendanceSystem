class Model:

    def __init__(self, id: str, userIds: list, encodings: list, createTime: int, updateTime: int):
        self.encodings = encodings
        self.userIds = userIds
        self.updateTime = updateTime
        self.createTime = createTime
        self.id = id

    def addFeature(self, userId, encoding):
        self.userIds.append(userId)
        self.encodings.append(encoding)
