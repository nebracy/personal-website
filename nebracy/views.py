from datetime import datetime
import hashlib
import hmac
import os
from flask import render_template, url_for, redirect, flash, request, jsonify, abort
from flask_mail import Message
from nebracy import app, db, mail
from .forms import ContactForm
from .models import Commit


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
            return redirect(url_for('index'))
    return render_template('index.html', form=form, title="Home", commits=commits)


@app.route('/webhook', methods=['POST'])
def webhook():
    if "X-Hub-Signature" not in request.headers:
        abort(400, "Missing header")
    elif "X-GitHub-Event" not in request.headers:
        abort(400, "Missing header")

    if request.headers["X-GitHub-Event"] == 'ping':
        return jsonify({}), 200
    elif request.headers["X-GitHub-Event"] == 'push':

        signature = request.headers['X-Hub-Signature']
        sha, signature = signature.split('=')
        if sha != "sha1":
            abort(400)

        secret = str.encode(os.environ['GITHUB_HOOK_SECRET'])

        hashhex = hmac.new(secret, request.data, hashlib.sha1).hexdigest()

        if not hmac.compare_digest(hashhex, signature):
            abort(400)

        payload = request.get_json()
        for commit in payload['commits']:
            pre_date = commit['timestamp']
            date = datetime.fromisoformat(pre_date)
            msg = commit['message']
            name = payload['repository']['name']
            url = payload['repository']['url']
            c = Commit(name, url, date, msg)
            db.session.add(c)
        db.session.commit()
        return jsonify({}), 200

    else:
        abort(400)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Page Not Found"), 404

