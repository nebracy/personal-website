from flask import url_for
from nebracy import create_app


def test_config_development(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == 'sqlite:///:memory:'
    assert not app.config["S3_FOLDER"]
    assert not app.config["SERVER_NAME"]
    assert app.static_url_path == ""


def test_config_staging():
    app = create_app('staging')
    app.config["SERVER_NAME"] = 'test.nicolebracy.com'
    with app.app_context():
        assert app.config["S3_FOLDER"] == 'static'
        assert app.config["ENV"] == 'production'
        assert url_for('home.index', _external=True, _scheme='https') == 'https://test.nicolebracy.com/'
        assert url_for('static', filename='favicon.ico', _external=True, _scheme='https') == 'https://static.test.nicolebracy.com/staging/favicon.ico'


def test_config_production():
    app = create_app('production')
    app.config["SERVER_NAME"] = 'nicolebracy.com'
    with app.app_context():
        assert app.config["S3_FOLDER"] == 'static/production'
        assert app.config["ENV"] == 'production'
        assert url_for('home.index', _external=True, _scheme='https') == 'https://nicolebracy.com/'
        assert url_for('static', filename='favicon.ico', _external=True, _scheme='https') == 'https://static.nicolebracy.com/favicon.ico'

