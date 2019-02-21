class UserFeature:

    def __init__(self, id: str, userId: str, imageId: str, feature, createTime: int, updateTime: int):
        self.imageId = imageId
        self.createTime = createTime
        self.feature = feature
        self.userId = userId
        self.id = id
