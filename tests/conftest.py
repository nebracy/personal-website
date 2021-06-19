import pytest
from nebracy import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app('development', '', 'static')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    yield app.test_client()
