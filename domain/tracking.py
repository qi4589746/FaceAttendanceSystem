class Tracking:

    def __init__(self, id: str, userId: str, subjectId: str, createTime: int, deviceMacAddress: str, updateTime: int):
        self.updateTime = updateTime
        self.deviceMacAddress = deviceMacAddress
        self.createTime = createTime
        self.subjectId = subjectId
        self.userId = userId
        self.id = id
