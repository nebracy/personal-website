from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()


def create_app(config: str = 'Production') -> Flask:
    static_folder = 'static' if config.capitalize() == 'Development' else None

    app = Flask(__name__, static_url_path='', static_folder=static_folder)
    app.config.from_object(f'config.{config.capitalize()}')

    if config.capitalize() != 'Development':
        app.static_folder = app.config.get('S3_FOLDER')
        app.add_url_rule(f'{app.config.get("STATIC_PATH")}/<path:filename>',
                         endpoint='static',
                         view_func=app.send_static_file,
                         subdomain='static')
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from nebracy.home.views import home
        from nebracy.apps.views import apps
        from nebracy.errors.handlers import errors

        app.register_blueprint(home)
        app.register_blueprint(apps)
        app.register_blueprint(errors)

        db.create_all()
        return app
