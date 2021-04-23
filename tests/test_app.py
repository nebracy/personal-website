from flask import url_for


def test_home_get(client):
    """Given When Then"""
    assert client.get('/').status_code == 200
    response = client.get(url_for('home.index', _external=True, _scheme='https'))
    assert response.status_code == 200
    assert b"Welcome!" in response.data
    assert url_for('home.index', _external=True, _scheme='https') == 'https://localhost/'
    assert url_for('static', filename='favicon.ico', _external=True, _scheme='https') == 'https://localhost/favicon.ico'



