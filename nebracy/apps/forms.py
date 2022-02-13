from flask_wtf import FlaskForm
import re
from wtforms import DecimalField, DecimalRangeField, FieldList, FormField, IntegerField, IntegerRangeField, RadioField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Optional, Length, NoneOf, ValidationError, Regexp

ingredients = ['flour', 'water', 'yeast', 'salt', 'oil', 'sugar']


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


class NoneOfRegexp(NoneOf):
    def __init__(self, values, message=None, values_formatter=None):
        super().__init__(values, message, values_formatter)

    def __call__(self, form, field):
        for list_item in self.values:
            regex = re.compile(f'({list_item})$', re.IGNORECASE)
            match = regex.match(field.data or "")
            if match:
                message = self.message
                if message is None:
                    message = field.gettext("Ingredient is already included.")
                raise ValidationError(message % dict(values=self.values_formatter(self.values)))
        return


class OptionalForm(FlaskForm):
    opt_name = StringField('Ingredient', description='Ingredient', validators=[Regexp("^[a-zA-Z\-( )'&]*$"), NoneOfRegexp(ingredients), Optional(), Length(0, 50)])
    opt_num = DecimalField('Percent', description='Ingredient', validators=[NumberRange(0, 50)])


class DoughCalculatorForm(FlaskForm):
    choice = RadioField('TF/Weight', choices=['Dough Weight', 'Thickness Factor'], default='Thickness Factor', validators=[InputRequired()])
    dough_wt = DecimalField('Dough Weight', validators=[RequiredIf(), NumberRange(1, 20000)])
    g_oz = RadioField('Grams/Ounces', choices=['oz', 'grams'], default='grams', validators=[RequiredIf()])
    thk_factor = DecimalRangeField('Thickness Factor', validators=[RequiredIf(), NumberRange(0.07, 0.1)])
    pizza_size = IntegerField('Pizza Size (in)', validators=[RequiredIf(), NumberRange(12, 22)])
    pizza_num = IntegerField('Pizza(s)', validators=[InputRequired(), NumberRange(1, 25)])
    water = IntegerRangeField('Hydration', description='Ingredient', validators=[InputRequired(), NumberRange(55, 70)])
    yeast = DecimalField('Yeast %', description='Ingredient', validators=[InputRequired(), NumberRange(0, 3)])
    salt = DecimalField('Salt %', description='Ingredient', validators=[InputRequired(), NumberRange(0, 4)])
    oil = DecimalField('Oil %', description='Ingredient', validators=[NumberRange(0, 8)])
    sugar = DecimalField('Sugar %', description='Ingredient', validators=[NumberRange(0, 4)])
    opt = FieldList(FormField(OptionalForm), min_entries=3, max_entries=3)
    calculate = SubmitField('Calculate')
