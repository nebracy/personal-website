import pytest
from flask import url_for


payload = {"ref": "refs/heads/master", "repository": {
        "name": "personal-website",
        "url": "https://github.com/nebracy/personal-website"},
        "commits": [{
            "id": "b550065594f767a9275b4c9a18810fd2d1479b74",
            "message": "Rename config class names",
            "timestamp": "2019-12-29T21:36:16-05:00"}]}


def test_home_get(client):
    """Given When Then"""
    home_url = url_for('home.index', _external=True, _scheme='https')
    assert home_url == 'https://localhost/'
    assert client.get(home_url).status_code == 200
    assert b"Welcome!" in client.get(home_url).data
    assert url_for('static', filename='favicon.ico', _external=True, _scheme='https') == 'https://localhost/favicon.ico'


def test_webhook_get(client):
    response = client.get('/webhook')
    assert response.status_code == 404


def test_webhook_ping_header(client):
    headers = {'X-GitHub-Event': 'ping'}
    response = client.post('/webhook', headers=headers)
    assert response.status_code == 200

