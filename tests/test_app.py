import pytest
from flask import url_for


def test_home_get(client):
    """Given When Then"""
    home_url = url_for('home.index', _external=True, _scheme='https')
    assert home_url == 'https://localhost/'
    assert client.get(home_url).status_code == 200
    assert b"Welcome!" in client.get(home_url).data
    assert url_for('static', filename='favicon.ico', _external=True, _scheme='https') == 'https://localhost/favicon.ico'
