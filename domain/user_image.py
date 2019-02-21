class UserImage:

    def __init__(self, id: str, userId: str, imageId: str, createTime: int, updateTime: int):
        self.updateTime = updateTime
        self.createTime = createTime
        self.imageId = imageId
        self.userId = userId
        self.id = id
