from flask import Blueprint, render_template, redirect, url_for
from nebracy.apps.forms import DoughCalculatorForm


apps = Blueprint('apps', __name__, subdomain='app')


@apps.get('/')
def index():
    return "<h1>TODO</h1>"


@apps.route('/pizza', methods=['GET', 'POST'])
def pizza():
    dough = {'Flour': {'Percent': 100}}
    form = DoughCalculatorForm()
    if form.validate_on_submit():
        dough |= {x.name: {'Percent': float(x.data)} for x in form if x.description}

    return render_template('apps/pizza.html', title="NY Pizza Dough Calculator", form=form, dough=dough)
