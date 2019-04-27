import hashlib
import hmac
import os
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify, abort
from forms import ContactForm
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True, static_url_path='')
app.config.from_object('config.ProductionConfig')
app.config.from_pyfile('config.py', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///github.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mail = Mail(app)


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    msg = db.Column(db.String(75), nullable=False)

    def __init__(self, name, url, date, msg):
        self.name = name
        self.url = url
        self.date = date
        self.msg = msg

    def __repr__(self):
        return f'<Commit {self.name}, {self.date}, {self.msg}>'


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Page Not Found"), 404


if __name__ == "__main__":
    app.run(debug=True)
