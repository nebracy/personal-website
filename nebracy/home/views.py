from os import getenv
from flask import (abort, Blueprint, current_app as app, jsonify, render_template,
                   redirect, request, url_for)
from sqlalchemy.exc import OperationalError
from nebracy.home.forms import ContactForm
from nebracy.home.models import Commit, update_table
from nebracy.home.utils import validate_github_headers, send_email, IncorrectGithubHeaderError, IncorrectGithubSecretError


home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    try:
        db_commits = Commit.query.order_by(Commit.date.desc()).limit(3).all()
    except OperationalError:
        print('Missing commit table')
        db_commits = []
    form = ContactForm()
    if form.validate_on_submit():
        send_email(app, form)
        return redirect(url_for('home.index', _external=True, _scheme='https', _anchor='contact'))
    return render_template('index.html', form=form, title="Home", commits=db_commits, config=getenv('FLASK_CONFIG'))


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

    update_table()
    return jsonify({}), 200
