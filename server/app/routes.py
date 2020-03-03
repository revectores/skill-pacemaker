from app import app,db
from werkzeug.urls import url_parse
from flask import render_template,redirect,flash,url_for,request
from flask_login import login_required,current_user,login_user
from app.forms import LoginForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/community/')
@app.route('/community/index')
def community_index():
    return render_template('community_index.html')

@app.route('/domain/select')
@login_required
def domain_select():
    return render_template('select.html',uid = 'Edwin Sha')

@app.route('/domain/dashboard')
@login_required
def domain_dashboard():
    return render_template('dashboard.html',uid = 'Edwin Sha')

@app.route('/community/new_thread')
@login_required
def community_new():
    return render_template('new_thread.html',uid = 'Edwin Sha')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',uid = 'Edwin Sha')
