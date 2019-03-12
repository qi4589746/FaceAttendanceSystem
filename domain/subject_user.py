class SubjectUser:

    def __init__(self, id: str, userId: str, subjectId: str, createTime: int, updateTime: int, role: int):
        self.updateTime = updateTime
        self.createTime = createTime
        self.subjectId = subjectId
        self.userId = userId
        self.role = role
        self.id = id

# Role: 1: admin, 2: guest
