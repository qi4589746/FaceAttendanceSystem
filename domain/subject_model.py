class SubjectModel:

    def __init__(self, id: str, subjectId: str, modelId: str, createTime: int, updateTime: int):
        self.createTime = createTime
        self.modelId = modelId
        self.id = id
        self.subjectId = subjectId
        self.updateTime = updateTime
