import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.environ["APP_NAME"]

FLASK_ENV = os.environ["FLASK_ENV"]
FLASK_RUN_PORT = os.environ["FLASK_RUN_PORT"]
FLASK_DEBUG = os.environ["FLASK_DEBUG"]

APP_SECRET_KEY = os.environ["APP_SECRET_KEY"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

JWT_EXPIRE_TOKEN = int(os.environ["JWT_EXPIRE_TOKEN"])

NAME = os.environ["DB_USERNAME"]
PASSWORD = os.environ["PWD_DB"]
NAME_DB = os.environ["NAME_DB"]
HOST = os.environ["DB_HOST"]

URL_FRONTEND = os.environ["URL_FRONTEND"]

ID_CODE_TWO_FACTOR = 1
ID_CODE_RESET_PASSWORD = 2

USER_EMAIL = str(os.environ["USER_EMAIL"])
PASSWORD_EMAIL = str(os.environ["PASSWORD_EMAIL"])

CONTENT_EMAIL_CODE_TEMPLATE = """
    <h1>Ola,</h1>
    <h1>Seu código de verificação é:</h1>
    <h2>{cod}</h2>
    """
    
CONTENT_EMAIL_RECOVER_PASSWORD = """
    <h1>Ola,</h1>
    <h1>Copie o link abaixo e cole em outra aba para resetar a senha</h1>
    <h2>{token}</h2>
    """


# NAME = 'root'
# PASSWORD = 'admin'
# NAME_DB = 'workstation'
# HOST = 'localhost'