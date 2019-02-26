import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
THREADED = True

ADMINS = frozenset(['jihung.mycena@gmail.com'])
SECRET_KEY = '6zA3wNkfRm'

MONGO_URI = 'mongodb://localhost:27017/faceMongo'
# "mongodb://localhost:27017/myDatabase"

CSRF_ENABLED = True
CSRF_SESSION_KEY = "6zA3wNkfRm"

# https://randomkeygen.com/
UPLOAD_FOLDER_IMAGE = "./temp/image/"
