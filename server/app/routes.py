from app import app, db
from werkzeug.urls import url_parse
from flask import render_template, redirect, flash, url_for, request, session, make_response
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Domain, Material, Record, Node
from io import BytesIO
from app.utils import new_verify_code, send_email, is_valid_email, test_recommend
import os
from markdown import markdown
from time import time, localtime, strftime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', auth=current_user.is_authenticated)


@app.route('/code')
def code():
    image, code = new_verify_code()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['image'] = code
    return response


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return render_template('login.html', form=form)
        if user.auth == False:
            flash('Unauthenticated email address.')
            return render_template('login.html', form=form)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return render_template('register.html', form=form)
        if not is_valid_email(form.mail_addr.data):
            flash('Invalid email address.')
            return render_template('register.html', form=form)
        user = User(username=form.username.data,
                    email=form.mail_addr.data, auth=False, gender=2,
                    avatar_name='/static/avatar/default.jpg', io='0.0')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.get_registration_token()
        send_email('Verify', app.config['MAIL_USERNAME'], [user.email], token,
                   render_template('mail.html', token=token))
        flash('Please finish registration with the verification URL in your email address.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/register/<token>')
def register_verify(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_registration_token(token)
    if not user:
        return redirect(url_for('index'))
    user.auth = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user,
                           gender=['女', '男', '神秘生物'][user.gender])


@app.route('/new_profile', methods=['GET', 'POST'])
@login_required
def new_profile():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    form = EditProfileForm(io=user.io, gender=str(user.gender))
    if form.validate_on_submit():
        if not form.avatar.data is None:
            avt = form.avatar.data
            if not avt.filename == '':
                avt.filename = user.username
                fn = 'app/static/avatar/' + avt.filename + '.jpg'
                avt.save(fn)
                user.avatar_name = '/static/avatar/' + avt.filename + '.jpg'
        user.gender = int(form.gender.data)
        user.io = form.io.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profile', username=user.username))
    return render_template('new_profile.html', form=form, user=user)


@app.route('/community/')
@app.route('/community/index')
def community_index():
    return render_template('community_index.html')


@app.route('/domain/select')
@login_required
def domain_select():
    # 人工在前端添加领域
    return render_template('select.html')


@app.route('/domain/dashboard')
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
    return render_template('dashboard.html', learning_mats=mats, finished_doms=[], recs=recs)


@app.route('/domain/index/<domain_name>')
@login_required
def domain_index(domain_name):
    domain = Domain.query.filter_by(name=domain_name).first_or_404()
    return render_template('domain_index.html', domain=domain, learning=233, finished=2333)


@app.route('/domain/learn/<mat_id>')
@login_required
def domain_learn(mat_id):
    mat = Material.query.filter_by(id=mat_id).first_or_404()
    node = Node.query.filter_by(id=mat.node).first_or_404()
    dom = Domain.query.filter_by(id=node.domain_id).first_or_404()
    md_file = open('app/' + mat.material_file)
    record = Record(timestamp=time(), user_id=current_user.id, score=-1, mat_id=mat.id)
    db.session.add(record)
    db.session.commit()
    return render_template('domain_learn.html', md=md_file.read(), material=mat,
                           domain=dom, node=node)


@app.route('/domain/learn/next/<node_id>')
@login_required
def get_next(node_id):
    record = Record(timestamp=time(), user_id=current_user.id, score=100, node_id=node_id)
    db.session.add(record)
    db.session.commit()
    return redirect('/domain/learn/' + str(test_recommend(int(node_id))))


@app.route('/domain/test/<name>')
@login_required
def domain_test(name):
    return redirect('/domain/learn/next/' + str(Node.query.filter_by(name=name).first_or_404().id))
    # return render_template('domain_test.html', node = Node.query.filter_by(name = name).first_or_404())


@app.route('/community/new_thread')
@login_required
def community_new():
    return render_template('new_thread.html', uid='Edwin Sha')
