from flask_wtf import FlaskForm
from wtforms import DecimalField, DecimalRangeField, FieldList, IntegerField, IntegerRangeField, RadioField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Optional


class RequiredIf:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        choice = form['choice'].data
        if field.id in ['thk_factor', 'pizza_size'] and choice == 'Thickness Factor':
            InputRequired().__call__(form, field)
        elif field.id in ['dough_wt', 'g_oz'] and choice == 'Dough Weight':
            InputRequired().__call__(form, field)
        else:
            Optional().__call__(form, field)


class DoughCalculatorForm(FlaskForm):
    choice = RadioField('TF/Weight', choices=['Dough Weight', 'Thickness Factor'], default='Thickness Factor', validators=[InputRequired()])
    dough_wt = DecimalField('Dough Weight', validators=[RequiredIf(), NumberRange(1, 20000)])
    g_oz = RadioField('Grams/Ounces', choices=['oz', 'grams'], default='grams', validators=[RequiredIf()])
    thk_factor = DecimalRangeField('Thickness Factor', validators=[RequiredIf(), NumberRange(0.07, 0.1)])
    pizza_size = IntegerField('Pizza Size (in)', validators=[RequiredIf(), NumberRange(12, 22)])
    pizza_num = IntegerField('Pizza(s)', validators=[InputRequired(), NumberRange(1, 25)])
    water = IntegerRangeField('Water %', description='Ingredient', validators=[InputRequired(), NumberRange(55, 70)])
    yeast = DecimalField('Yeast %', description='Ingredient', validators=[InputRequired(), NumberRange(0, 3)])
    salt = DecimalField('Salt %', description='Ingredient', validators=[InputRequired(), NumberRange(0, 4)])
    oil = DecimalField('Oil %', description='Ingredient', validators=[Optional(), NumberRange(0, 8)])
    sugar = DecimalField('Sugar %', description='Ingredient', validators=[Optional(), NumberRange(0, 4)])
    calculate = SubmitField('Calculate')
