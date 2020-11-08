import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
CSRFProtect(app)
Bootstrap(app)
Markdown(app)

from app import routes, models, forms
from app.db_init import db_init

if os.environ.get("DB_INIT"):
	db_init()
	