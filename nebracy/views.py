from datetime import datetime
import hashlib
import hmac
import os
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify, abort
from flask_mail import Message
from nebracy import forms, mail, models, static_subdomain


home = Blueprint('home', __name__)
errors = Blueprint('errors', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    commits = models.Commit.query.order_by(models.Commit.date.desc()).limit(3).all()
    contact_form = forms.ContactForm()
    if contact_form.validate_on_submit():
        if contact_form.website.data == '':
            msg = Message(contact_form.subj.data,
                          sender=(contact_form.name.data, 'contact@nebracy.com'),
                          recipients=['contact@nebracy.com'],
                          reply_to=contact_form.email.data)
            msg.body = contact_form.msg.data
            mail.send(msg)
            flash(f'Email sent, thank you!')
            return redirect(url_for('index', _external=True, _scheme='https'))
    return render_template('index.html', form=contact_form, title="Home", commits=commits, static=static_subdomain)


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
            abort(400)

    payload = request.get_json()
    if payload['ref'] == 'refs/heads/master':
        try:
            for commit in payload['commits']:
                pre_date = commit['timestamp']
                commit_id = commit['id']
                date = datetime.fromisoformat(pre_date)
                msg = commit['message']
                name = payload['repository']['name']
                url = payload['repository']['url']
                c = models.Commit(commit_id, name, url, date, msg)
                models.db.session.add(c)
            models.db.session.commit()
        except IntegrityError:
            abort(400, "Database is already up to date")
        return jsonify({}), 200
    else:
        abort(400, "Commits from this push are from another branch besides master")


@errors.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Page Not Found"), 404


# todo create 500.html
# @errors.errorhandler(500)
# def internal_server_error(error):
#     return render_template('500.html', title="Internal Server Error"), 500

