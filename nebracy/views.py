from datetime import datetime
import hashlib
import hmac
import os
from sqlalchemy.exc import IntegrityError
from flask import render_template, url_for, redirect, flash, request, jsonify, abort
from flask_mail import Message
from nebracy import app, mail, static
from .forms import ContactForm
from .models import db, Commit


@app.route('/', methods=['GET', 'POST'])
def index():
    commits = Commit.query.order_by(Commit.date.desc()).limit(3).all()
    form = ContactForm()
    if form.validate_on_submit():
        if form.website.data == '':
            msg = Message(form.subj.data, sender=(form.name.data, 'contact@nebracy.com'), recipients=['contact@nebracy.com'], reply_to=form.email.data)
            msg.body = form.msg.data
            mail.send(msg)
            flash(f'Email sent, thank you!')
            return redirect(url_for('index', _external=True, _scheme='https'))
    return render_template('index.html', form=form, title="Home", commits=commits, static=static)


@app.route('/webhook', methods=['POST'])
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
                c = Commit(commit_id, name, url, date, msg)
                db.session.add(c)
            db.session.commit()
        except IntegrityError:
            abort(400, "Database is already up to date")
        return jsonify({}), 200
    else:
        abort(400, "Commits from this push are from another branch besides master")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Page Not Found"), 404

