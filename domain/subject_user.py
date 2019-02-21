class SubjectUser:

    def __init__(self, id: str, userId: str, subjectId: str, createTime: int, updateTime: int):
        self.updateTime = updateTime
        self.createTime = createTime
        self.subjectId = subjectId
        self.userId = userId
        self.id = id
