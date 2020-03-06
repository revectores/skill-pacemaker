from app import app,db
from werkzeug.urls import url_parse
from flask import render_template,redirect,flash,url_for,request,session,make_response
from flask_login import login_required,current_user,login_user, logout_user
from app.forms import LoginForm,RegistrationForm
from app.models import User
from io import BytesIO
from app.utils import new_verify_code

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return render_template('login.html', form=form)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return render_template('register.html', form=form)
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

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
    return render_template('profile.html')
