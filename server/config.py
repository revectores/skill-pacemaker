import os
from datetime import timedelta


class Config:
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zlynb'
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/skip.db"
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'SQLALCHEMY_DATABASE_URI') or 'mysql://root@106.15.206.77:3306/test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USERNAME = '396707050@qq.com'
    MAIL_PASSWORD = 'lnwkaytlhrvqbgeb'
    MAIL_USE_SSL = 1
    MAIL_DEBUG = 1

    MAX_CONTENT_LENGTH = 1024 * 1024 * 5

    SEND_FILE_MAX_AGE_DEFAULT = timedelta(milliseconds=1)
