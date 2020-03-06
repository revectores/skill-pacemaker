from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import re

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    '''email = db.Column(db.String(64),index = True,unique = True)
    gender = db.Column(db.Integer)
    auth = db.Column(db.Integer,index = True)
    avatar_name = db.Column(db.Integer,unique = True)
    io = db.Column(db.String(255))'''

    def is_valid_email(self):
        if len(self.email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) != None:
                return True
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))