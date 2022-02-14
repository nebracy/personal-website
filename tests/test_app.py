import pytest
from flask import url_for
from nebracy import mail


payload = {"ref": "refs/heads/master", "repository": {
        "full_name": "nebracy/personal-website",
        "url": "https://github.com/nebracy/personal-website"},
        "commits": [{
            "id": "b550065594f767a9275b4c9a18810fd2d1479b74",
            "message": "Rename config class names",
            "timestamp": "2019-12-29T21:36:16-05:00"}]}


def test_home_get(client):
    """Given When Then"""
    home_url = url_for('home.index', _external=True, _scheme='https')
    assert client.get(home_url).status_code == 200
    assert b"Welcome!" in client.get(home_url).data
    assert url_for('static', filename='favicon.ico', _external=True, _scheme='https') == 'https://local.nicolebracy.com:443/favicon.ico'


# TODO
# def test_send_email():
#     """"""
#     with mail.record_messages() as outbox:
#         mail.send_message(subject='Contact Form: Testing',
#                           body='This is a test.',
#                           recipients=['contact@nicolebracy.com'])
#
#         assert len(outbox) == 1
#         assert outbox[0].subject == 'Contact Form: Testing'


def test_webhook_get(client):
    """"""
    response = client.get('/webhook')
    assert response.status_code == 404


def test_webhook_ping_header(client):
    """"""
    headers = {'X-GitHub-Event': 'ping'}
    response = client.post('/webhook', headers=headers)
    assert response.status_code == 200
    assert b'{\n  "ping": "Success"\n}' in response.data


@pytest.mark.parametrize("headers", [{'': ''}, {'X-GitHub-Event': ''}, {'X-GitHub-Event': 'junk'}])
def test_webhook_wrong_headers(client, headers):
    """"""
    response = client.post('/webhook', headers=headers)
    assert response.status_code == 400
    assert b"Missing correct headers" in response.data


@pytest.mark.parametrize("headers", [{'X-GitHub-Event': 'push', 'X-Hub-Signature': 'sha1='},
                                     {'X-GitHub-Event': 'push', 'X-Hub-Signature': ''}])
def test_webhook_wrong_github_secret(client, headers):
    """"""
    response = client.post('/webhook', headers=headers)
    assert response.status_code == 400
    assert b"Incorrect secret" in response.data


def test_webhook_not_master_branch(client):
    """"""
    payload_stub = {'ref': 'refs/heads/staging'}
    headers = {'X-GitHub-Event': 'push', 'X-Hub-Signature': 'sha1=c7abcc644d90c1a4a3ee67bd0ecf8665ea1d7347'}
    response = client.post('/webhook', headers=headers, json=payload_stub)
    assert response.status_code == 403
    assert b"Push was not to the master branch." in response.data


def test_webhook_commit(client):
    """"""
    headers = {'X-GitHub-Event': 'push', 'X-Hub-Signature': 'sha1=b2f3b3cef75ff72ba41a49175f5b19f400ae2e99'}
    response = client.post('/webhook', headers=headers, json=payload)
    assert response.status_code == 200
    assert b"" in response.data
