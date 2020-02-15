import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__, instance_relative_config=True, static_url_path='')
app.add_url_rule('/<path:filename>',
                 endpoint='static',
                 subdomain='<subdomain>',
                 view_func=app.send_static_file)
env = os.getenv('FLASK_ENV', 'Production')
app.config.from_object(f'config.{env}')
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
mail = Mail(app)

from . import views

db.create_all()
