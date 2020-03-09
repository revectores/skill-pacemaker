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
    
    gender = db.Column(db.Integer,index = True)
    avatar_name = db.Column(db.String(255))
    io = db.Column(db.String(255))
    

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

class Domain(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(255),nullable = True)
    tree_file = db.Column(db.String(255),nullable = True)

class Node(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    test_file = db.Column(db.String(255),nullable = True)
    domain_id = db.Column(db.Integer,db.ForeignKey('domain.id'),index = True)

class Link(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    prev = db.Column(db.Integer,db.ForeignKey('node.id'),index = True)
    nxt = db.Column(db.Integer,db.ForeignKey('node.id'),index = True)

class Material(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    node = db.Column(db.Integer,db.ForeignKey('node.id'),nullable = True,index = True)
    material_file = db.Column(db.String(255),nullable = True)
    creator_id = db.Column(db.Integer,nullable = True,index = True)

class Record(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    timestamp = db.Column(db.Integer,index = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),index = True)
    is_test = db.Column(db.Integer,index = True)
    mat_id = db.Column(db.Integer,db.ForeignKey('material.id'),index = True,nullable = True)
    score = db.Column(db.Integer,index = True,nullable = True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
