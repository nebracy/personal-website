from os import getenv
from flask import (abort, Blueprint, current_app as app, jsonify, render_template,
                   redirect, request, url_for)
from sqlalchemy.exc import IntegrityError, OperationalError
from nebracy.forms import ContactForm
from nebracy.models import Commit, GithubCommits, GithubTokenNotFoundError
from nebracy.utils import validate_github_headers, send_email, IncorrectGithubHeaderError, IncorrectGithubSecretError


home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    try:
        db_commits = Commit.query.order_by(Commit.date.desc()).limit(3).all()
    except OperationalError:
        print('Missing commit table')
        db_commits = []
    if ContactForm().validate_on_submit():
        send_email(app, ContactForm())
        return redirect(url_for('home.index', _external=True, _scheme='https', _anchor='contact'))
    config = getenv('FLASK_CONFIG')
    return render_template('index.html', form=ContactForm(), title="Home", commits=db_commits, config=config)


@home.post('/webhook')
def webhook():
    try:
        if request.headers.get("X-GitHub-Event") == 'ping':
            return jsonify(ping="Success"), 200
        validate_github_headers()
    except (IncorrectGithubSecretError, IncorrectGithubHeaderError) as e:
        abort(400, e)

    payload = request.get_json()
    if payload['ref'] != 'refs/heads/master':
        abort(403, "Commits from this push are from another branch besides master")

    try:
        github = GithubCommits()
        github.get_commits_from_payload(payload)
        github.add_to_db()
    except IntegrityError:
        abort(400, "Database is already up to date")
    except GithubTokenNotFoundError as e:
        abort(400, e)
    return jsonify({}), 200
