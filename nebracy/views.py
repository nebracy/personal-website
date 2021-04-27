from datetime import datetime
import hashlib
import hmac
import os
from sqlalchemy.exc import IntegrityError, OperationalError
from flask import (abort, Blueprint, current_app as app, jsonify, render_template,
                   redirect, flash, request, url_for)
from flask_mail import Message
from nebracy import forms, mail, models


home = Blueprint('home', __name__)
errors = Blueprint('errors', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    try:
        commits = models.Commit
        db_commits = commits.query.order_by(commits.date.desc()).limit(3).all()
    except OperationalError:
        print('Missing commit table')
        db_commits = []
    contact_form = forms.ContactForm()
    if contact_form.validate_on_submit():
        msg = Message(contact_form.subj.data,
                      sender=(contact_form.name.data, app.config['MAIL_DEFAULT_SENDER']),
                      recipients=[app.config['MAIL_DEFAULT_SENDER']],
                      reply_to=contact_form.email.data)
        msg.body = contact_form.msg.data
        mail.send(msg)
        flash(f'Email sent, thank you!')
        return redirect(url_for('home.index', _external=True, _scheme='https'))
    return render_template('index.html', form=contact_form, title="Home", commits=db_commits)


@home.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers["X-GitHub-Event"] == 'ping':
            return jsonify({}), 200
        elif request.headers["X-GitHub-Event"] != 'push':
            raise KeyError
        signature = request.headers['X-Hub-Signature']
        sha, signature = signature.split('sha1=')
    except (KeyError, ValueError):
        abort(400, "Missing correct headers")
    else:
        secret = str.encode(os.getenv('GITHUB_HOOK_SECRET'))
        hashhex = hmac.new(secret, request.data, hashlib.sha1).hexdigest()
        if not hmac.compare_digest(hashhex, signature):
            abort(400, "Incorrect secret")

    payload = request.get_json()
    g = models.GithubCommits()
    if payload['ref'] == 'refs/heads/master':
        try:
            g.add_to_db(payload)
        except IntegrityError:
            abort(400, "Database is already up to date")
        return jsonify({}), 200
    else:
        abort(400, "Commits from this push are from another branch besides master")


@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title="Page Not Found"), 404


@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title="Internal Server Error"), 500

