from flask import Blueprint, render_template


apps = Blueprint('apps', __name__, subdomain='app')


@apps.get('/')
def index():
    return "<h1>TODO</h1>"


@apps.route('/pizza', methods=['GET', 'POST'])
def pizza():
    return render_template('pizza.html', title="NY Pizza Dough Calculator")
