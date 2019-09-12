import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__, instance_relative_config=True, static_url_path='')
app.config.from_object(os.getenv('FLASK_ENV', 'config.DevelopmentConfig'))
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
mail = Mail(app)

from . import views

db.create_all()
