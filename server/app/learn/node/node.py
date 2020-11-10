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
from app.models import User, Domain, Material, Record, Section, SectionLink, Node, NodeLink, Read, Test, UserDomain, UserNode, UserRead, UserTest
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend, get_nodes_coordinates


node = Blueprint('node', __name__)


@node.route('/<int:node_id>')
@login_required
def node_index(node_id):
	read_id = 1
	return redirect(f'/learn/node/read/{read_id}', '302')


@node.route('/read/<int:read_id>')
@login_required
def node_read(read_id):
	read = Read.query.get_or_404(read_id)
	node = Node.query.get_or_404(read.node_id)
	section = Section.query.get_or_404(node.section_id)
	domain = Domain.query.get_or_404(section.domain_id)

	md_file = open('/Users/rex/Library/Mobile Documents/com~apple~CloudDocs/dev/skill-pacemaker/server/app/static/material/read/1.html')
	# open('../../static/material/read/1.md')
	return render_template('learn/node/read.html', md=md_file.read(), domain=domain, node=node)


@node.route('/test/<int:test_id>')
@login_required
def node_test(test_id):
	pass