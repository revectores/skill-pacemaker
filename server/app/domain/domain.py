import os
from markdown import markdown
from io import BytesIO
from time import time, localtime, strftime

from werkzeug.urls import url_parse
from flask import render_template, redirect, flash, url_for, request, session, make_response, Blueprint, jsonify
from flask_login import login_required, current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Domain, Material, Record, Section, SectionLink, Node, NodeLink, UserNode
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend, get_nodes_coordinates


domain = Blueprint('domain', __name__)
section = Blueprint('section', __name__)


@app.template_filter('test')
def tt(t):
    return t + '11'


@domain.route('/dashboard')
@login_required
def domain_dashboard():
    # TODO:获得学习材料，完成领域，学习记录矩阵
    mats = []

    recs = []
    for rec in Record.query.filter_by(user_id=current_user.id).order_by(Record.timestamp.desc()).all():
        r = []  # 时间，领域，知识点，内容
        r.append(strftime("%Y-%m-%d %H:%M:%S", localtime(rec.timestamp)))
        if rec.score == -1:
            mat = Material.query.filter_by(id=rec.mat_id).first_or_404()
            node = Node.query.filter_by(id=mat.node).first_or_404()
            domain = Domain.query.filter_by(id=node.domain_id).first_or_404()
            r.append(domain.name)
            r.append(node.name)
            r.append('阅读材料')
        else:
            node = Node.query.filter_by(id=rec.node_id).first_or_404()
            domain = Domain.query.filter_by(id=node.domain_id).first_or_404()
            r.append(domain.name)
            r.append(node.name)
            r.append('测验得分 ' + str(rec.score))
        recs.append(r)
        if len(recs) == 15:
            break
    return render_template('domain/dashboard.html', learning_mats=mats, finished_doms=[], recs=recs)



@domain.route('/select')
@login_required
def domain_select():
    domains = Domain.query.all()
    return render_template('domain/select.html', domains=domains)



@domain.route('/<int:domain_id>')
@login_required
def domain_index(domain_id):
    domain = Domain.query.filter_by(id=domain_id).first_or_404()
    return render_template('domain/index.html', domain=domain, learning=233, finished=2333)



@domain.route('/tree/<int:domain_id>')
@login_required
def domain_tree(domain_id):
    sections = Section.query.filter_by(domain_id=domain_id)
    links = SectionLink.query.filter_by(domain_id=domain_id)
    # nodes = Section.query().filter_by(domain_id=domain_id).join(Node, Node.section_id==Section.id)
    nodes = db.session.query(Node.id).\
            join(Section, Section.id == Node.section_id).\
            filter(Section.domain_id == domain_id)

    user_nodes = db.session.query(Node.id, Section.id).\
                    join(Section, Section.id == Node.section_id).\
                    join(UserNode, UserNode.id == Node.id).\
                    filter(Section.domain_id == domain_id).\
                    filter(UserNode.master == True)

    for user_node in user_nodes:
        pass
    # print(len(list(nodes)), len(list(user_nodes)))

    section_ids = [section.id for section in sections]
    link_tuples = [(link.source, link.target) for link in links]

    nodes_coordinates = get_nodes_coordinates(section_ids, link_tuples)

    section_graph = {
        'nodes': [],
        'links': []
    }

    for section in sections:
        section_graph['nodes'].append({
            'id': str(section.id),
            'name': section.name,
            'x': nodes_coordinates[section.id][0] * 100,
            'y': nodes_coordinates[section.id][1] * 100,
            'itemStyle': {
                'normal': {
                    # 'color': 'rgb(0, 105, 216)'
                }
            }
        })

    for link in links:
        section_graph['links'].append({
            'source': str(link.source),
            'target': str(link.target)
        })

    return jsonify(section_graph)



@domain.route('/section/<int:section_id>')
@login_required
def section_index(section_id):
    section = Section.query.filter_by(id=section_id).first_or_404()

    return render_template('domain/section.html', section=section)



@domain.route('/section/tree/<int:section_id>')
@login_required
def section_tree(section_id):
    nodes = Node.query.filter_by(section_id=section_id)
    links = NodeLink.query.filter_by(section_id=section_id)

    node_ids = [node.id for node in nodes]
    link_tuples = [(link.source, link.target) for link in links]

    nodes_coordinates = get_nodes_coordinates(node_ids, link_tuples)

    node_graph = {
        'nodes': [],
        'links': []
    }

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


@domain.route('/pretest/<int:domain_id>')
@login_required
def pretest(domain_id):
    print(domain_id)
    domain = Domain.query.filter_by(id=domain_id).first_or_404()
    return render_template('domain/pretest.html', domain=domain)



@domain.route('/learn/<mat_id>')
@login_required
def domain_learn(mat_id):
    mat = Material.query.filter_by(id=mat_id).first_or_404()
    node = Node.query.filter_by(id=mat.node).first_or_404()
    dom = Domain.query.filter_by(id=node.domain_id).first_or_404()
    md_file = open('app/' + mat.material_file)
    record = Record(timestamp=time(), user_id=current_user.id, score=-1, mat_id=mat.id)
    db.session.add(record)
    db.session.commit()
    return render_template('domain/learn.html', md=md_file.read(), material=mat,
                           domain=dom, node=node)



@domain.route('/learn/next/<node_id>')
@login_required
def get_next(node_id):
    record = Record(timestamp=time(), user_id=current_user.id, score=100, node_id=node_id)
    db.session.add(record)
    db.session.commit()
    return redirect('/domain/learn/' + str(test_recommend(int(node_id))))



@domain.route('/test/<name>')
@login_required
def domain_test(name):
    return redirect('/domain/learn/next/' + str(Node.query.filter_by(name=name).first_or_404().id))
    # return render_template('domain_test.html', node = Node.query.filter_by(name = name).first_or_404())
