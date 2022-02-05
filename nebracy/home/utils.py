from flask import flash, request
from flask_mail import Message
import hashlib
import hmac
from os import getenv
from nebracy import mail


def send_email(app, contact_form):
    msg = Message(f'Contact Form: {contact_form.subj.data}',
                  sender=(contact_form.name.data, app.config['MAIL_DEFAULT_SENDER']),
                  recipients=[app.config['MAIL_RECIPIENT']],
                  reply_to=contact_form.email.data)
    msg.body = contact_form.msg.data
    mail.send(msg)
    flash(f'Email sent, thank you!')


class IncorrectGithubHeaderError(Exception):
    """Raised when one or more Github headers are missing or incorrect."""
    pass


class IncorrectGithubSecretError(Exception):
    """Raised when the Github secret is incorrect."""
    pass


def validate_github_headers() -> None:
    if request.headers.get("X-GitHub-Event") != 'push':
        raise IncorrectGithubHeaderError("Missing correct headers")

    signature = request.headers['X-Hub-Signature']
    secret = str.encode(getenv('GITHUB_HOOK_SECRET'))
    hashhex = hmac.new(secret, request.data, hashlib.sha1).hexdigest()
    if not hmac.compare_digest(hashhex, signature.removeprefix('sha1=')):
        raise IncorrectGithubSecretError("Incorrect secret")
