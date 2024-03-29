from decimal import Decimal
from flask import Blueprint, render_template, redirect, session, url_for, request, abort
import math
from nebracy.apps.forms import DoughCalculatorForm


apps = Blueprint('apps', __name__, subdomain='app')


@apps.route('/', methods=['GET', 'POST'])
@apps.route('/pizza-dough-calculator', methods=['GET', 'POST'])
def pizza():
    form = DoughCalculatorForm(flour=100)
    if form.validate_on_submit():
        dough = {ing.name: {'Percent': ing.data} for ing in form if ing.description}

        for ing in form.opt.data + [form.yeast.data]:
            if ing['iname']:
                dough[ing['iname']] = {}
                dough[ing['iname']]['Percent'] = ing['num']

        if form.dough_wt.data and form.choice.data == 'Dough Weight':
            dough_wt = form.dough_wt.data
        else:
            radius2 = (form.pizza_size.data / 2) ** 2
            dough_wt = form.thk_factor.data * Decimal(math.pi * radius2)
        total_pct = sum(val['Percent'] for val in dough.values())
        flour_wt = dough_wt * form.pizza_num.data / (total_pct / 100)

        dough |= {'total': {'Percent': total_pct}}
        for kv in dough.values():
            weight = flour_wt * (kv['Percent']) / 100
            kv['Grams'] = kv['Ounces'] = weight
            if form.g_oz.data == 'g' and form.choice.data == 'Dough Weight':
                kv |= {'Ounces': weight * Decimal(0.03527396195)}
            else:
                kv |= {'Grams': weight * Decimal(28.349523125)}
        session['recipe'] = dough
        return redirect(url_for('apps.pizza', _external=True, _scheme='https', _anchor='recipe'))
    dough = total = None
    if recipe := session.get('recipe'):
        total = recipe.pop('total')
        list_order = ['flour', 'water', 'IDY', 'ADY', 'salt', 'olive_oil', 'sugar']
        list_order.extend(k for k in recipe.keys() - list_order)
        dough = {k: recipe[k] for k in list_order if recipe.get(k)}
    return render_template('apps/pizza.html', form=form, dough=dough, total=total)


@apps.get('/pizza-dough-calculator/add-ingredient')
@apps.get('/pizza-dough-calculator/add-ingredient/<int:opt_entry>')
def add_ingredient(opt_entry=0):
    if 'HX_request' not in request.headers:
        abort(400)

    form = DoughCalculatorForm()
    try:
        opt = form.opt.entries.pop(opt_entry)
    except IndexError:
        abort(404)
    else:
        opt_entry += 1
        return render_template('apps/add.html', opt=opt, opt_entry=opt_entry, max_opt=form.opt.max_entries)
