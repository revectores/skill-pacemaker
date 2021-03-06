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


class MaterialState(Enum):
    EDITING   = 0 
    REVIEWING = 1
    REVIEWED  = 2


class UserLearnLogType(Enum):
    LEARN  = 0
    TEST   = 1
    REVIEW = 2


@dataclass
class User(UserMixin, db.Model):
    id: int
    username: str
    password_hash: str
    email: str
    auth: int
    gender: int
    avatar_name: str
    io: str

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
    color: str

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(20))
    description = db.Column(db.String(255), nullable=True)
    node_count  = db.Column(db.Integer, default=0)
    color       = db.Column(db.String(255))


@dataclass
class Section(db.Model):
    id: int
    domain_id: int
    name: str

    id        = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), index=True)
    name      = db.Column(db.String(255), index=True)


@dataclass
class Node(db.Model):
    id: int
    section_id: int
    name: str

    id         = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)
    name       = db.Column(db.String(255), index=True)


@dataclass
class SectionLink(db.Model):
    id: int
    domain_id: int
    source: int
    target: int

    id        = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    source    = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)
    target    = db.Column(db.Integer, db.ForeignKey('section.id'), index=True)


@dataclass
class NodeLink(db.Model):
    id: int
    section_id: int
    source: int
    target: int

    id         = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    source     = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)
    target     = db.Column(db.Integer, db.ForeignKey('node.id'), index=True)


@dataclass
class Material(db.Model):
    id: int
    node_id: int
    contributor_id: int
    description: str
    reader_count: int
    length: int
    score: int
    average_spent_time: timedelta
    reviewer_count: int

    id             = db.Column(db.Integer, primary_key=True)
    node_id        = db.Column(db.Integer)
    contributor_id = db.Column(db.Integer)
    state          = db.Column(db.Enum(MaterialState), default=MaterialState.REVIEWED)
    description    = db.Column(db.String(255))
    reader_count   = db.Column(db.Integer)
    length         = db.Column(db.Integer)
    score          = db.Column(db.Integer)
    average_spent_time = db.Column(db.Interval)
    reviewer_count = db.Column(db.Integer)
    vote           = db.Column(db.Integer)



@dataclass
class Test(db.Model):
    id: int
    node_id: int
    contributor_id: int

    id             = db.Column(db.Integer, primary_key=True)
    node_id        = db.Column(db.Integer)
    contributor_id = db.Column(db.Integer)
    state          = db.Column(db.Enum(MaterialState), default=MaterialState.REVIEWED)
    description    = db.Column(db.String(255))
    reader_count   = db.Column(db.Integer)
    length         = db.Column(db.Integer)
    score          = db.Column(db.Integer)
    averge_spent_time = db.Column(db.Interval)
    reviewer_count = db.Column(db.Integer)
    vote           = db.Column(db.Integer)



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


@dataclass
class UserLearnLog(db.Model):
    id: int
    type: int
    user_id: int
    domain_id: int
    section_id: int
    node_id: int
    material_id: int
    start: datetime
    end: datetime

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


