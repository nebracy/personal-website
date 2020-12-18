import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()

config_env = os.getenv('FLASK_ENV', 'Production')
if config_env == 'Production':
    static_subdomain = 'static'
elif config_env == 'Staging' or 'Development':
    static_subdomain = 'static2'


def create_app():
    app = Flask(__name__, static_url_path='')
    app.add_url_rule('/<path:filename>',
                     endpoint='static',
                     subdomain='<static>',
                     view_func=app.send_static_file)

    app.config.from_object(f'config.{os.getenv("FLASK_ENV", "Production")}')

    # if env == 'Staging':
    #     app.url_map.default_subdomain = 'test'
    # elif env == 'Development':
    #     app.url_map.default_subdomain = 'local'

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from nebracy import views
        app.register_blueprint(views.home)
        app.register_blueprint(views.errors)

        db.create_all()
        return app


# @app.url_value_preprocessor
# def before_route(endpoint, values):
#     if values is not None:
#         values.pop('static', None)

