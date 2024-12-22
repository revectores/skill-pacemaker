import os
from markdown import markdown
from io import BytesIO
from time import time, localtime, strftime

from werkzeug.urls import url_parse
from flask import render_template, redirect, flash, url_for, request, session, make_response, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EditorForm, MaterialForm
from app.models import User, Domain, Material, Record, Node
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend


community = Blueprint('community', __name__)


@community.route('/')
@community.route('/index')
def community_index():
    return render_template('community/index.html')


@community.route('/new_thread')
@login_required
def community_new():
    form = EditorForm()
    return render_template('community/new_thread.html', uid='Edwin Sha',form = form)

@community.route('/t/<tid>')
def community_thread(tid):
    form = EditorForm()
    return render_template('community/thread.html',form = form)

@community.route('/new_material')
@login_required
def mat_new():
    form = MaterialForm()
    return render_template('community/new_material.html', uid='Edwin Sha',form = form)

@community.route('/new_test')
@login_required
def test_new():
    form = MaterialForm()
    return render_template('community/new_test.html', uid='Edwin Sha',form = form)