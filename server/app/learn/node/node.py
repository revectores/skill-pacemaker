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
	user_domain = UserDomain.query.get_or_404(section.domain_id)

	read_html_file = open(app.root_path + f"/static/read/{read_id}.html")
	return render_template('learn/node/read.html', read_html=read_html_file.read(),
						   domain=domain, section=section, node=node, user_domain=user_domain)



@node.route('/test/<int:node_id>')
@login_required
def node_test(node_id):
	node = Node.query.get_or_404(node_id)
	section = Section.query.get_or_404(node.section_id)
	domain = Domain.query.get_or_404(section.domain_id)
	user_domain = UserDomain.query.get_or_404(section.domain_id)

	return render_template('learn/node/test.html',
						   domain=domain, section=section, node=node, user_domain=user_domain)

