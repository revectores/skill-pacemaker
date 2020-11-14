import os
from app import db
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import re, jwt
from time import time
from datetime import datetime, timedelta
from config import Config
from dataclasses import dataclass
from enum import Enum


class DomainState(Enum):
    UNSELECTED = 0
    SELECTED   = 1
    PRETESTED  = 2
    COMPLETED  = 3



class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    email         = db.Column(db.String(64), index=True, unique=True)
    auth          = db.Column(db.Integer, index=True)

    gender        = db.Column(db.Integer, index=True)
    avatar_name   = db.Column(db.String(255))
    io            = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_registration_token(self, expires_in=6000):
        return jwt.encode({
                'registration': self.id,
                'exp': time() + expires_in
            },
            Config.SECRET_KEY,
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_registration_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['registration']
        except:
            return
        return User.query.get(id)

@dataclass
class Domain(db.Model):
    id: int
    name: str
    description: str
    node_count: int

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(20))
    description = db.Column(db.String(255), nullable=True)
    node_count  = db.Column(db.Integer, default=0)


class Section(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), index=True)
    name      = db.Column(db.String(255), index=True)


class Node(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)
    name       = db.Column(db.String(255), index=True)


class SectionLink(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    source    = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)
    target    = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)


class NodeLink(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    source     = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)
    target     = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)


class Material(db.Model):
    id: int
    node_id: int
    contributor_id: int
    description: str
    reader_count: int
    length: int
    score: int
    average_spent_time: timedelta

    id             = db.Column(db.Integer, primary_key=True)
    node_id        = db.Column(db.Integer)
    contributor_id = db.Column(db.Integer)
    description    = db.Column(db.String(255))
    reader_count   = db.Column(db.Integer)
    length         = db.Column(db.Integer)
    score          = db.Column(db.Integer)
    average_spent_time = db.Column(db.Interval)



class Test(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    node_id        = db.Column(db.Integer)
    contributor_id = db.Column(db.Integer)


class Record(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, index=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    mat_id    = db.Column(db.Integer, db.ForeignKey('material.id'), index=True, nullable=True)
    node_id   = db.Column(db.Integer, db.ForeignKey('node.id'), index=True, nullable=True)
    score     = db.Column(db.Integer, index=True)  # -1为学习，>=0为考试


@dataclass
class UserDomain(db.Model):
    id: int
    user_id: int
    domain_id: int
    state: int
    mastered_node_count: id

    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'))
    domain_id           = db.Column(db.Integer, db.ForeignKey('domain.id'))
    state               = db.Column(db.Enum(DomainState), default=DomainState.UNSELECTED)
    mastered_node_count = db.Column(db.Integer, default=0)


class UserSection(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    # progress = db.Column(db.)


class UserNode(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    node_id  = db.Column(db.Integer, db.ForeignKey('node.id'))
    mastered = db.Column(db.Boolean)


class UserMaterial(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))


class UserTest(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))


class UserLearnLog(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    type        = db.Column(db.Integer)    # 0 for learn, 1 for test
    user_id     = db.Column(db.Integer)
    domain_id   = db.Column(db.Integer)
    section_id  = db.Column(db.Integer)
    node_id     = db.Column(db.Integer)
    material_id = db.Column(db.Integer)
    start       = db.Column(db.DateTime)
    end         = db.Column(db.DateTime)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


