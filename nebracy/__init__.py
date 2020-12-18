import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__, static_url_path='')
    app.config.from_object(f'config.{os.getenv("FLASK_ENV", "Production")}')

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from nebracy import views
        app.register_blueprint(views.home)
        app.register_blueprint(views.errors)

        db.create_all()
        return app
