class User:

    def __init__(self, id: str, name: str, description: str, createTime: int, updateTime: int):
        self.updateTime = updateTime
        self.createTime = createTime
        self.description = description
        self.name = name
        self.id = id
