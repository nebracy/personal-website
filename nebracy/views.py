from os import getenv
from flask import (abort, Blueprint, current_app as app, jsonify, render_template,
                   redirect, request, url_for)
from sqlalchemy.exc import IntegrityError, OperationalError
from nebracy.forms import ContactForm
from nebracy.models import Commit, GithubCommits, GithubTokenNotFoundError
from nebracy.utils import validate_github_headers, send_email, IncorrectGithubHeaderError, IncorrectGithubSecretError


home = Blueprint('home', __name__)
errors = Blueprint('errors', __name__)


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


# @home.post('/webhook')
# def webhook():
#     try:
#         if request.headers["X-GitHub-Event"] == 'ping':
#             return jsonify(ping="Success"), 200
#         elif request.headers["X-GitHub-Event"] != 'push':
#             raise KeyError
#         signature = request.headers['X-Hub-Signature']
#         sha, signature = signature.split('sha1=')
#     except (KeyError, ValueError):
#         abort(400, "Missing correct headers")
#     else:
#         secret = str.encode(getenv('GITHUB_HOOK_SECRET'))
#         hashhex = hmac.new(secret, request.data, hashlib.sha1).hexdigest()
#         if not hmac.compare_digest(hashhex, signature):
#             abort(400, "Incorrect secret")
#
#     payload = request.get_json()
#     if payload['ref'] == 'refs/heads/master':
#         github_commits = GithubCommits()
#         try:
#             github_commits.add_to_db(payload)
#         except IntegrityError:
#             abort(400, "Database is already up to date")
#         except GithubTokenNotFoundError:
#             abort(400, "The environment variable GITHUB_TOKEN is not set")
#         return jsonify({}), 200
#     else:
#         abort(403, "Commits from this push are from another branch besides master")

@home.post('/webhook')
def webhook():
    try:
        if request.headers.get("X-GitHub-Event") == 'ping':
            return jsonify(ping="Success"), 200
        validate_github_headers()
    except (IncorrectGithubSecretError, IncorrectGithubHeaderError) as e:
        abort(400, e)

    payload = request.get_json()
    if payload['ref'] == 'refs/heads/master':
        github_commits = GithubCommits()
        try:
            github_commits.add_to_db(payload)
        except IntegrityError:
            abort(400, "Database is already up to date")
        except GithubTokenNotFoundError:
            abort(400, "The environment variable GITHUB_TOKEN is not set")
        return jsonify({}), 200
    else:
        abort(403, "Commits from this push are from another branch besides master")


@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title="Page Not Found"), 404


@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title="Internal Server Error"), 500

