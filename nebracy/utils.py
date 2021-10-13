from flask import flash
from flask_mail import Message
from nebracy import mail


def send_email(app, contact_form):
    msg = Message(f'Contact Form: {contact_form.subj.data}',
                  sender=(contact_form.name.data, app.config['MAIL_DEFAULT_SENDER']),
                  recipients=[app.config['MAIL_RECIPIENT']],
                  reply_to=contact_form.email.data)
    msg.body = contact_form.msg.data
    mail.send(msg)
    flash(f'Email sent, thank you!')
