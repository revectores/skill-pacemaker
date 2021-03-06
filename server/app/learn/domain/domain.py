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
from app.models import DomainState, UserLearnLogType
from app.models import User, Domain, Material, Record, Section, SectionLink, Node, NodeLink, UserDomain, UserNode, UserLearnLog
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend, get_nodes_coordinates
from app.learn.node.node import node_index


domain = Blueprint('domain', __name__)
domain_api = Blueprint('domain_api', __name__)



@app.route('/learn/dashboard')
@login_required
def domain_dashboard():
    # TODO:获得学习材料，完成领域，学习记录矩阵
    mats = []

    recs = []
    """
    for rec in Record.query.filter_by(user_id=current_user.id).order_by(Record.timestamp.desc()).all():
        r = []  # 时间，领域，知识点，内容
        r.append(strftime("%Y-%m-%d %H:%M:%S", localtime(rec.timestamp)))
        if rec.score == -1:
            mat = Material.query.filter_by(id=rec.mat_id).first_or_404()
            node = Node.query.get_or_404(mat.node)
            section = Section.query.get_or_404(node.section_id)
            domain = Domain.query.get_or_404(section.domain_id)
            r.append(domain.name)
            r.append(node.name)
            r.append('阅读材料')
        else:
            node = Node.query.get_or_404(rec.node_id)
            section = Section.query.get_or_404(node.section_id)
            domain = Domain.query.get_or_404(section.domain_id)
            r.append(domain.name)
            r.append(node.name)
            r.append('测验得分 ' + str(rec.score))
        recs.append(r)
        if len(recs) == 15:
            break
    """
    return render_template('learn/dashboard.html')



@domain.route('/<int:domain_id>')
@login_required
def domain_index(domain_id):
    return render_template('learn/domain/index.html')



@domain.route('/select')
@login_required
def domain_select():
    return render_template('learn/domain/select.html')



@domain_api.route('/list')
def domain_list():
    query = Domain.query.all()

    domains = {
        domain.id: {
            'domain_id':    domain.id,
            'name':         domain.name,
            'description':  domain.description,
            'node_count':   domain.node_count
        } for domain in query
    }

    return jsonify(domains)



@domain_api.route('/list/<int:domain_id>')
def domain_list_one():
    query = Domain.query.get_or_404(domain_id)

    domain = {
        'domain_id':    query.id,
        'name':         query.name,
        'description':  query.description,
        'node_count':   query.node_count
    }
 
    return jsonify(domain)



@domain_api.route('/user/list')
@login_required
def user_domain_list():
    query = db.session.query(Domain, UserDomain).\
            filter(Domain.id == UserDomain.id).\
            filter(UserDomain.user_id == current_user.id).all()

    user_domains = {
        domain.id: {
            'domain_id':           domain.id,
            'name':                domain.name,
            'description':         domain.description,
            'node_count':          domain.node_count,
            'user_id':             user_domain.user_id,
            'state':               user_domain.state.value,
            'mastered_node_count': user_domain.mastered_node_count
        }
        for domain, user_domain in query
        # if user_domain.state.value >= DomainState.SELECTED.value
    }

    return jsonify(user_domains)



@domain_api.route('/user/list/<int:domain_id>')
@login_required
def user_domain_list_one(domain_id):
    query = db.session.query(Domain, UserDomain).\
            filter(Domain.id == domain_id).\
            filter(UserDomain.user_id == current_user.id).\
            filter(Domain.id == UserDomain.domain_id).first_or_404()

    domain, user_domain = query
    user_domain = {
        'domain_id':    domain.id,
        'name':         domain.name,
        'description':  domain.description,
        'node_count':   domain.node_count,
        'user_id':      user_domain.user_id,
        'state':        user_domain.state.value,
        'mastered_node_count': user_domain.mastered_node_count
    }
    return jsonify(user_domain)



@domain.route('/next/<int:domain_id>')
@login_required
def domain_next(domain_id):
    next_node_id = 1
    return redirect(f'/learn/node/{next_node_id}', '302')



@domain_api.route('/tree/<int:domain_id>')
@login_required
def domain_tree(domain_id):
    sections = Section.query.filter_by(domain_id=domain_id)
    links = SectionLink.query.filter_by(domain_id=domain_id)
    # nodes = Section.query().filter_by(domain_id=domain_id).join(Node, Node.section_id==Section.id)
    section_nodes = db.session.query(Section.id, Node.id).\
                    join(Section, Section.id == Node.section_id).\
                    filter(Section.domain_id == domain_id)

    user_section_nodes = db.session.query(Section.id, Node.id).\
                         join(Section, Section.id == Node.section_id).\
                         join(UserNode, UserNode.id == Node.id).\
                         filter(Section.domain_id == domain_id).\
                         filter(UserNode.mastered == True)

    user_domain = UserDomain.query.filter_by(domain_id=domain_id, user_id=current_user.id).first()

    section_node_counts = Counter([section_node[0] for section_node in section_nodes])
    user_section_node_counts = Counter([user_section_node[0] for user_section_node in user_section_nodes])

    # print(section_node_counts)
    # print(user_section_node_counts)
    # print(len(list(nodes)), len(list(user_nodes)))

    section_ids = [section.id for section in sections]
    link_tuples = [(link.source, link.target) for link in links]

    nodes_coordinates = get_nodes_coordinates(section_ids, link_tuples)

    section_graph = {
        'nodes': [],
        'links': []
    }
    colors = ['rgb(200, 200, 200)', 'rgb(100, 141, 200)', 'rgb(10, 20, 200)']


    for section in sections:
        print(user_domain.state)
        if user_domain.state.value == DomainState.UNSELECTED.value:
            color = colors[0]
        elif user_section_node_counts[section.id] == 0:
            color = colors[0]
        elif user_section_node_counts[section.id] < section_node_counts[section.id]:
            color = colors[1]
        elif user_section_node_counts[section.id] == section_node_counts[section.id]:
            color = colors[2]
        else:
            color = colors[0]

        section_graph['nodes'].append({
            'id': str(section.id),
            'name': section.name,
            'x': nodes_coordinates[section.id][0] * 100,
            'y': nodes_coordinates[section.id][1] * 100,
            'itemStyle': {
                'normal': {
                    'color': color,
                }
            }
        })

    for link in links:
        section_graph['links'].append({
            'source': str(link.source),
            'target': str(link.target)
        })

    return jsonify(section_graph)



@domain.route('/pretest/<int:domain_id>')
@login_required
def pretest(domain_id):
    domain = Domain.query.filter_by(id=domain_id).first_or_404()
    return render_template('learn/domain/pretest.html', domain=domain)



@domain.route('/pretest/submit/<int:domain_id>')
@login_required
def pretest_submit(domain_id):
    user_domain = UserDomain.query.filter_by(user_id=current_user.id, domain_id=domain_id).first_or_404()
    user_domain.state = DomainState.PRETESTED
    db.session.commit()

    return ('', 204)



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
    return render_template('learn/domain/learn.html', md=md_file.read(), material=mat,
                           domain=dom, node=node)



@domain.route('/learn/next/<node_id>')
@login_required
def get_next(node_id):
    record = Record(timestamp=time(), user_id=current_user.id, score=100, node_id=node_id)
    db.session.add(record)
    db.session.commit()
    return redirect('/learn/domain/learn/' + str(test_recommend(int(node_id))))



@domain.route('/test/<name>')
@login_required
def domain_test(name):
    return redirect('/learn/domain/learn/next/' + str(Node.query.filter_by(name=name).first_or_404().id))
    # return render_template('domain_test.html', node = Node.query.filter_by(name = name).first_or_404())




@domain_api.route('/log')
@login_required
def domain_logs():
    query = UserLearnLog.query.\
            filter_by(user_id=current_user.id).\
            all()

    return jsonify(query)



@domain_api.route('/log/<int:domain_id>')
@login_required
def domain_log(domain_id):
    query = UserLearnLog.query.\
            filter_by(user_id=current_user.id).\
            filter_by(domain_id=domain_id).\
            all()

    return jsonify(query)


