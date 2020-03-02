from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/domain/dashboard')
def domain_dashboard():
    return render_template('dashboard.html')

@app.route('/domain/select')
def domain_select():
    return render_template('select.html')

@app.route('/community/')
@app.route('/community/index')
def community_index():
    return render_template('community_index.html')


@app.route('/community/new_thread')
def community_new():
    return render_template('new_thread.html')

