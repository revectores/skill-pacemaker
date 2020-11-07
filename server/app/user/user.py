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


user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        """
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return render_template('user/register.html', form=form)
        if not is_valid_email(form.mail_addr.data):
            flash('Invalid email address.')
            return render_template('user/register.html', form=form)
        """
        user = User(username=form.username.data,
                    email=form.mail_addr.data, auth=False, gender=2,
                    avatar_name='/static/avatar/default.jpg', io='0.0')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.get_registration_token()
        """
        send_email('Verify', app.config['MAIL_USERNAME'], [user.email], token,
                   render_template('user/mail.html', token=token))
        flash('Please finish registration with the verification URL in your email address.')
        """
        return redirect(url_for('login'))
    return render_template('user/register.html', form=form)


@user.route('/register/<token>')
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

        """
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return render_template('user/login.html', form=form)

        if user.auth == False:
            flash('Unauthenticated email address.')
            return render_template('user/login.html', form=form)
        """

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@user.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/profile.html', user=user,
                           gender=['女', '男', '神秘生物'][user.gender])


@user.route('/new_profile', methods=['GET', 'POST'])
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
    return render_template('user/new_profile.html', form=form, user=user)
