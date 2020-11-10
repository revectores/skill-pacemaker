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


section = Blueprint('section', __name__)


@section.route('/<int:section_id>')
@login_required
def section_index(section_id):
    section = Section.query.filter_by(id=section_id).first_or_404()
    return render_template('learn/section/index.html', section=section)


@section.route('/tree/<int:section_id>')
@login_required
def section_tree(section_id):
    nodes = Node.query.filter_by(section_id=section_id)
    links = NodeLink.query.filter_by(section_id=section_id)

    node_ids = [node.id for node in nodes]
    link_tuples = [(link.source, link.target) for link in links]
    nodes_coordinates = get_nodes_coordinates(node_ids, link_tuples)
    node_graph = {'nodes': [], 'links': []}

    for node in nodes:
        node_graph['nodes'].append({
            'id': str(node.id),
            'name': node.name,
            'x': nodes_coordinates[node.id][0] * 100,
            'y': nodes_coordinates[node.id][1] * 100
        })

    for link in links:
        node_graph['links'].append({
            'source': str(link.source),
            'target': str(link.target)
        })

    return jsonify(node_graph)
