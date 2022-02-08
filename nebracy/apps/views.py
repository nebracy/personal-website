from flask import Blueprint, render_template, redirect, url_for
import math
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

        if form.dough_weight.data:
            dough_weight = form.dough_weight.data
        else:
            radius2 = (form.pizza_size.data / 2) ** 2
            dough_weight = form.thickness_factor.data * (math.pi * radius2)
        total_percent = sum(v['Percent'] for v in dough.values())
        flour_weight = float(dough_weight) * form.pizza_num.data / (total_percent / 100)

        for kv in dough.values():
            weight = flour_weight * (kv['Percent']) / 100
            kv['Grams'] = kv['Ounces'] = weight
            if form.g_oz.data == 'grams':
                kv.update({'Ounces': weight * 0.03527396195})
            else:
                kv.update({'Grams': weight * 28.349523125})
    return render_template('apps/pizza.html', title="NY Pizza Dough Calculator", form=form, dough=dough)
