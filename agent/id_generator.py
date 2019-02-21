import uuid
import time


def generateId(prefix: str):
    return prefix + "-" + str(int(time.time()*100))[3:10] + "-" + str(uuid.uuid4())[-12:-1]
