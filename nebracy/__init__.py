import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()
static_folder = os.getenv('FLASK_STATIC_FOLDER', None)


def create_app():
    app = Flask(__name__, static_url_path='', static_folder=static_folder)
    app.config.from_object(f'config.{os.getenv("FLASK_CONFIG")}')
    s3_folder = app.config.get('S3_FOLDER')
    if not static_folder:
        app.static_folder = s3_folder
        app.add_url_rule('/<path:filename>',
                         endpoint='static',
                         view_func=app.send_static_file,
                         subdomain='static')
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from nebracy import views
        app.register_blueprint(views.home)
        app.register_blueprint(views.errors)

        db.create_all()
        return app
