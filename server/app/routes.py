import os
from markdown import markdown
from io import BytesIO
from time import time, localtime, strftime

from werkzeug.urls import url_parse
from flask import render_template, redirect, flash, url_for, request, session, make_response
from flask_login import login_required, current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Domain, Material, Record, Node
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend

from app.user.user import user
from app.learn.domain.domain import domain, domain_api
from app.learn.section.section import section, section_api
from app.learn.node.node import node, node_api
from app.community.community import community

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(domain, url_prefix='/learn/domain')
app.register_blueprint(section, url_prefix='/learn/section')
app.register_blueprint(node, url_prefix='/learn/node')
app.register_blueprint(community, url_prefix='/community')

# app.register_blueprint(user_api, url_prefix='/api/user')
app.register_blueprint(domain_api, url_prefix='/api/learn/domain')
app.register_blueprint(section_api, url_prefix='/api/learn/section')
app.register_blueprint(node_api, url_prefix='/api/learn/node')
# app.register_blueprint(community_api, url_prefix='/api/community')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', auth=current_user.is_authenticated)


@app.route('/code')
def code():
    image, code = new_verify_code()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['image'] = code
    return response


