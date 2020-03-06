import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zlynb'
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql://qwq:396707050@139.196.179.104:3306/test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True 

    AUTH_PICTURE_PATH = os.environ.get('AUTH_PICTURE_PATH') or '~/auth/'

    MAIL_SERVER='smtp.qq.com'
    MAIL_PORT=465
    MAIL_USERNAME='396707050@qq.com'
    MAIL_PASSWORD='lnwkaytlhrvqbgeb'
    MAIL_USE_SSL=1
    MAIL_DEBUG=1