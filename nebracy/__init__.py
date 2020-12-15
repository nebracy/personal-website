import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__, instance_relative_config=True, static_url_path='')
app.add_url_rule('/<path:filename>',
                 endpoint='static',
                 subdomain='<static>',
                 view_func=app.send_static_file)


@app.url_value_preprocessor
def before_route(endpoint, values):
    if values is not None:
        values.pop('static', None)


env = os.getenv('FLASK_ENV', 'Production')
app.config.from_object(f'config.{env}')
if env == 'Production':
    static = 'static'
else:
    static = 'static2'
    app.url_map.default_subdomain = 'test'
db = SQLAlchemy(app)
mail = Mail(app)

from . import views

db.create_all()
