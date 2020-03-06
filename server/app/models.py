from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import re,jwt
from time import time
from config import Config

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(64),index = True,unique = True)
    auth = db.Column(db.Integer,index = True)
    '''
    gender = db.Column(db.Integer)
    avatar_name = db.Column(db.Integer,unique = True)
    io = db.Column(db.String(255))
    '''

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_registration_token(self, expires_in= 6000):
        return jwt.encode(
            {'registration': self.id, 'exp': time() + expires_in},
            Config.SECRET_KEY, algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_registration_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY,
                algorithms=['HS256'])['registration']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))