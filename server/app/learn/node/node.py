import os
import json
from collections import Counter
from io import BytesIO
from time import time, localtime, strftime

from markdown import markdown
from werkzeug.urls import url_parse
from flask import render_template, redirect, flash, url_for, request, session, make_response, Blueprint, jsonify
from flask_login import login_required, current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Domain, Material, Record, Section, SectionLink, Node, NodeLink, UserDomain, UserNode
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend, get_nodes_coordinates


node = Blueprint('node', __name__)


@node.route('/<int:node_id>')
@login_required
def section_index(node_id):
    return ('', 204)
