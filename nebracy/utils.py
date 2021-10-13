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


# def validate_github_headers():
#     try:
#         if request.headers["X-GitHub-Event"] != 'push':
#             raise KeyError("Missing correct headers")
#         signature = request.headers['X-Hub-Signature']
#         # sha, signature = signature.split('sha1=')
#         signature = signature.removeprefix('sha1=')
#     except ValueError:
#         raise ValueError("Missing correct headers")
#     else:
#         secret = str.encode(getenv('GITHUB_HOOK_SECRET'))
#         hashhex = hmac.new(secret, request.data, hashlib.sha1).hexdigest()
#         if not hmac.compare_digest(hashhex, signature):
#             raise ValueError("Incorrect secret")

class IncorrectGithubHeaderError(Exception):
    pass


class IncorrectGithubSecretError(Exception):
    pass


def validate_github_headers():
    if request.headers.get("X-GitHub-Event") != 'push':
        raise IncorrectGithubHeaderError("Missing correct headers")

    signature = request.headers['X-Hub-Signature']
    secret = str.encode(getenv('GITHUB_HOOK_SECRET'))
    hashhex = hmac.new(secret, request.data, hashlib.sha1).hexdigest()
    if not hmac.compare_digest(hashhex, signature.removeprefix('sha1=')):
        raise IncorrectGithubSecretError("Incorrect secret")
