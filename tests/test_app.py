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


@pytest.mark.parametrize("headers", [{'': ''}, {'X-GitHub-Event': ''}, {'X-GitHub-Event': 'junk'}, {'X-GitHub-Event': 'push', 'X-Hub-Signature': ''}])
def test_webhook_wrong_headers(client, headers):
    response = client.post('/webhook', headers=headers)
    assert response.status_code == 400
    assert b"Missing correct headers" in response.data


def test_webhook_wrong_github_secret(client):
    headers = {'X-GitHub-Event': 'push', 'X-Hub-Signature': 'sha1='}
    response = client.post('/webhook', headers=headers)
    assert response.status_code == 400
    assert b"Incorrect secret" in response.data


def test_webhook_no_payload(client):
    """May add try except to code later"""
    headers = {'X-GitHub-Event': 'push', 'X-Hub-Signature': 'sha1=309013598748f3c03458df4c8e8e4e28415140d6'}
    with pytest.raises(KeyError):
        client.post('/webhook', headers=headers, json={})


def test_webhook_missing_commit_data(client):
    """May add try except to code later"""
    mock_payload = {'ref': 'refs/heads/master'}
    headers = {'X-GitHub-Event': 'push', 'X-Hub-Signature': 'sha1=59b4d890f67dc3d7e5ad534dbab78081696dd759'}
    with pytest.raises(KeyError):
        client.post('/webhook', headers=headers, json=mock_payload)
