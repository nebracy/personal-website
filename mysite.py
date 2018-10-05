from flask import Flask, render_template
from forms import ContactForm

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)


@app.route("/")
def index():
    form = ContactForm()
    return render_template('index.html', form=form, title="Home")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Page Not Found"), 404


if __name__ == "__main__":
    app.run(debug=True)
