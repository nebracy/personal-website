from flask import Flask, render_template, url_for, redirect
from forms import ContactForm
from flask_mail import Mail, Message

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

mail = Mail(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        if form.honey.data == '':
            msg = Message(form.subj.data, sender=(form.name.data, form.email.data), recipients=['contact@nebracy.com'],
                          reply_to=form.email.data)
            msg.body = form.msg.data
            mail.send(msg)
            return redirect(url_for('index'))
    return render_template('index.html', form=form, title="Home")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Page Not Found"), 404


if __name__ == "__main__":
    app.run(debug=True)
