from flask import flash
from flask_mail import Message
from nebracy import mail
from nebracy.forms import ContactForm


def send_email_form(app):
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        msg = Message(f'Contact Form: {contact_form.subj.data}',
                      sender=(contact_form.name.data, app.config['MAIL_DEFAULT_SENDER']),
                      recipients=[app.config['MAIL_RECIPIENT']],
                      reply_to=contact_form.email.data)
        msg.body = contact_form.msg.data
        mail.send(msg)
        flash(f'Email sent, thank you!')
