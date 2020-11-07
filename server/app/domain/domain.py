import os
from markdown import markdown
from io import BytesIO
from time import time, localtime, strftime

from werkzeug.urls import url_parse
from flask import render_template, redirect, flash, url_for, request, session, make_response, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Domain, Material, Record, Node
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend


domain = Blueprint('domain', __name__)


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
    # 人工在前端添加领域
    return render_template('domain/select.html')



@domain.route('/index/<domain_name>')
@login_required
def domain_index(domain_name):
    domain = Domain.query.filter_by(name=domain_name).first_or_404()
    return render_template('domain/index.html', domain=domain, learning=233, finished=2333)


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
