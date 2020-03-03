import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zlynb'
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql://qwq:396707050@127.0.0.1:3306/test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True 
