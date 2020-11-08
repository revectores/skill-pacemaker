import os
from app import db
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import re, jwt
from time import time
from config import Config


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(64), index=True, unique=True)
    auth = db.Column(db.Integer, index=True)

    gender = db.Column(db.Integer, index=True)
    avatar_name = db.Column(db.String(255))
    io = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_registration_token(self, expires_in=6000):
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(255), nullable=True)
    tree_file = db.Column(db.String(255), nullable=True)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), index=True)
    name = db.Column(db.String(255), index=True)


class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)
    name = db.Column(db.String(255), index=True)


class SectionLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    source = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)
    target = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)


class NodeLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    source = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)
    target = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=True, index=True)
    material_file = db.Column(db.String(255), nullable=True)
    creator_id = db.Column(db.Integer, nullable=True, index=True)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    mat_id = db.Column(db.Integer, db.ForeignKey('material.id'), index=True, nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'), index=True, nullable=True)
    score = db.Column(db.Integer, index=True)  # -1为学习，>=0为考试


class UserDomain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    pretest = db.Column(db.Boolean)


class UserSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    # progress = db.Column(db.)


class UserNode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    master = db.Column(db.Boolean)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


