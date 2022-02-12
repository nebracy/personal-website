from decimal import Decimal
from flask import Blueprint, render_template, redirect, session, url_for
import math
from nebracy.apps.forms import DoughCalculatorForm


apps = Blueprint('apps', __name__, subdomain='app')


@apps.get('/')
def index():
    return "<h1>TODO</h1>"


@apps.route('/pizza', methods=['GET', 'POST'])
def pizza():
    form = DoughCalculatorForm()
    if form.validate_on_submit():
        dough = {x.name: {'Percent': x.data} for x in form if x.description} | {'Flour': {'Percent': 100}}

        if form.dough_wt.data and form.choice.data == 'Dough Weight':
            dough_wt = form.dough_wt.data
        else:
            radius2 = (form.pizza_size.data / 2) ** 2
            dough_wt = form.thk_factor.data * Decimal(math.pi * radius2)
        total_pct = sum(v['Percent'] for v in dough.values())
        flour_wt = dough_wt * form.pizza_num.data / (total_pct / 100)

        dough |= {'Total': {'Percent': total_pct}}
        for kv in dough.values():
            weight = flour_wt * (kv['Percent']) / 100
            kv['Grams'] = kv['Ounces'] = weight
            if form.g_oz.data == 'grams' and form.choice.data == 'Dough Weight':
                kv |= {'Ounces': weight * Decimal(0.03527396195)}
            else:
                kv |= {'Grams': weight * Decimal(28.349523125)}
        session['recipe'] = dough
        return redirect(url_for('apps.pizza', _external=True, _scheme='https'))
    dough = {}
    if session.get('recipe'):
        dough = {k: session.get('recipe')[k] for k in ['Flour', 'water', 'yeast', 'salt', 'oil', 'sugar', 'Total']}
    return render_template('apps/pizza.html', title="NY Pizza Dough Calculator", form=form, dough=dough)
