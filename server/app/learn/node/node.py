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
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EditorForm, MaterialForm
from app.models import User, Domain, Material, Record, Section, SectionLink, Node, NodeLink, Material, Test, UserDomain, UserNode, UserMaterial, UserTest
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend, get_nodes_coordinates


node = Blueprint('node', __name__)
node_api = Blueprint('node_api', __name__)


@node_api.route('/')
def nodes():
    query = db.session.query(Node).all()
    nodes = {node.id: node for node in query}
    return jsonify(nodes)



@node.route('/<int:node_id>')
@login_required
def node_index(node_id):
	# material_id = 1
	# return redirect(f'/learn/node/material/{material_id}', '302')

	return render_template('learn/node/index.html')




@node_api.route('/<int:node_id>')
@login_required
def node_info(node_id):
	query = db.session.query(Domain, Section, Node, UserDomain).\
			filter(Node.id == node_id).\
			filter(Node.section_id == Section.id).\
			filter(Section.domain_id == Domain.id).\
			filter(UserDomain.domain_id == Domain.id).\
			filter(UserDomain.user_id == current_user.id).\
			first_or_404()

	domain, section, node_, user_domain = query

	node = {
		'id':			node_.id,
		'node_id':		node_.id,
		'name':			node_.name,
		'section_id':	section.id,
		'section_name': section.name,
		'domain_id':	domain.id,
		'domain_name':	domain.name,
		'domain_state': user_domain.state.value
	}

	return jsonify(node)


@node_api.route('/get_by_domain/<int:domain_id>')
def get_section_by_domain(domain_id):
    query = db.session.query(Node, Section).\
    		filter(Node.section_id == Section.domain_id).\
    		filter(Section.domain_id == domain_id).\
    		all()

    nodes_q = [q[0] for q in query]
    nodes = {node.id: node for node in nodes_q}

    return jsonify(nodes)



@node.route('/material/<int:material_id>')
@login_required
def node_material(material_id):
	material = Material.query.get_or_404(material_id)
	node = Node.query.get_or_404(material.node_id)
	section = Section.query.get_or_404(node.section_id)
	domain = Domain.query.get_or_404(section.domain_id)
	user_domain = UserDomain.query.get_or_404(section.domain_id)

	material_html_file = open(app.root_path + f"/static/material/{material_id}.html")
	return render_template('learn/node/material.html', material=material, material_html=material_html_file.read(),
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



@node.route('/materials/<int:node_id>')
@login_required
def html_material_list(node_id):
	return render_template('learn/node/material_list.html')



@node_api.route('/materials/<int:node_id>')
def get_materials(node_id):
	"""
	query = db.session.query(Material, UserMaterial).
			filter_by(Material.node_id == node_id).all()
			filter_by(UserMaterial.id == current_user.id).\
			filter_by(Material.id == UserMaterial.material_id).all()
	"""

	query = Material.query.filter_by(node_id=node_id).all()

	materials = {
		material.id : {
			'id':					material.id,
			'materid_id':			material.id,
			'node_id':				material.node_id,
			'contributor_id':		material.contributor_id,
			'description':			material.description,
			'reader_count':			material.reader_count,
			'length':				material.length,
			'score':				material.score,
			'average_spent_time':	material.average_spent_time
		}
		for material in query
	} 

	return jsonify(materials)



@node.route('/new_material')
def new_material():
	material_form = MaterialForm()
	return render_template('learn/node/new_material.html', uid='Edwin Sha', form=material_form)



@node.route('/new_test')
def new_test():
	material_form = MaterialForm()
	return render_template('learn/node/new_test.html', uid='Edwin Sha', form=material_form)



@node.route('/material_review')
def material_review():
	return render_template('learn/node/material_review.html')



@node.route('/test_review')
def test_review():
	return render_template('learn/node/test_review.html')



@node.route('/material_review_list/<int:node_id>')
def material_review_list(node_id):
	return render_template('learn/node/material_review_list.html')



@node.route('/test_review_list/<int:node_id>')
def test_review_list(node_id):
	return render_template('learn/node/test_review_list.html')
