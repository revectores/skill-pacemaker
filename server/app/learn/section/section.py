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
from app.models import DomainState
from app.models import User, Domain, Material, Record, Section, SectionLink, Node, NodeLink, UserDomain, UserNode
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend, get_nodes_coordinates


section = Blueprint('section', __name__)
section_api = Blueprint('section_api', __name__)


@section.route('/<int:section_id>')
@login_required
def section_index(section_id):
    return render_template('learn/section/index.html')



@section_api.route('/<int:section_id>')
def section_info(section_id):
    # query = db.session.query(section, usersection).\
    #         filter(section.id == section_id).\
    #         filter(section.id == usersection.section.id).\
    #         filter(usersection.id == current_user.id)
    # query = Section.query.filter_by(id=section_id).first_or_404()

    query = db.session.query(Domain, Section).\
            filter(Section.id == section_id).\
            filter(Domain.id == Section.domain_id).\
            first_or_404()

    domain, section_ = query

    section = {
        'id':           section_.id,
        'section_id':   section_.id,
        'name':         section_.name,
        'domain_id':    domain.id,
        'domain_name':  domain.name
    }

    return jsonify(section)



@section_api.route('/tree/<int:section_id>')
@login_required
def section_tree(section_id):
    nodes = Node.query.filter_by(section_id=section_id)
    links = NodeLink.query.filter_by(section_id=section_id)
    domain, user_domain, section = db.session.query(Domain, UserDomain, Section).\
                                   filter(Section.id == section_id).\
                                   filter(Domain.id == Section.domain_id).\
                                   filter(Domain.id == UserDomain.id).\
                                   first()

    user_nodes = db.session.query(Node, UserNode).\
                 filter(Node.section_id == section_id).\
                 filter(Node.id == UserNode.id)

    node_ids = [node.id for node in nodes]
    link_tuples = [(link.source, link.target) for link in links]
    nodes_coordinates = get_nodes_coordinates(node_ids, link_tuples)
    node_graph = {'nodes': [], 'links': []}

    print(domain.id, domain.name)

    colors = ['rgb(200, 200, 200)', 'rgb(10, 20, 200)']
    for (node, user_node) in user_nodes:
        if user_domain.state.value == DomainState.UNSELECTED.value:
            color = colors[0]
        elif user_node.mastered:
            color = colors[1]
        else:
            color = colors[0]

        node_graph['nodes'].append({
            'id': str(node.id),
            'name': node.name,
            'x': nodes_coordinates[node.id][0] * 100,
            'y': nodes_coordinates[node.id][1] * 100,
            'itemStyle': {
                'normal': {
                    'color': color
                }
            }
        })

    for link in links:
        node_graph['links'].append({
            'source': str(link.source),
            'target': str(link.target)
        })

    return jsonify(node_graph)



