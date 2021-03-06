import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.environ["APP_NAME"]

FLASK_ENV = os.environ["FLASK_ENV"]
FLASK_RUN_PORT = os.environ["FLASK_RUN_PORT"]
FLASK_DEBUG = os.environ["FLASK_DEBUG"]

APP_SECRET_KEY = os.environ["APP_SECRET_KEY"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

NAME = os.environ["DB_USERNAME"]
PASSWORD = os.environ["PWD_DB"]
NAME_DB = os.environ["NAME_DB"]
HOST = os.environ["DB_HOST"]


PASSWORD_EMAIL = os.environ["PASSWORD_EMAIL"]


# NAME = 'root'
# PASSWORD = 'admin'
# NAME_DB = 'workstation'
# HOST = 'localhost'