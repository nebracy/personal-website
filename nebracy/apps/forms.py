from flask_wtf import FlaskForm
from wtforms import DecimalField, DecimalRangeField, FieldList, IntegerField, IntegerRangeField, RadioField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Optional


class DoughCalculatorForm(FlaskForm):
    choice = RadioField('TF/Weight', choices=['Dough Weight', 'Thickness Factor'], default='Thickness Factor', validators=[InputRequired()])
    dough_weight = DecimalField('Dough Weight', validators=[Optional(), NumberRange(0.01, 20000)])
    g_oz = RadioField('Grams/Ounces', choices=['oz', 'grams'], validators=[Optional()])
    thickness_factor = DecimalRangeField('Thickness Factor', validators=[Optional(), NumberRange(0.07, 0.1)])
    pizza_size = IntegerField('Pizza Size (in)', validators=[Optional(), NumberRange(12, 22)])
    pizza_num = IntegerField('Pizza(s)', validators=[InputRequired(), NumberRange(1, 25)])
    water = IntegerRangeField('Water %', description='Ingredient', validators=[InputRequired(), NumberRange(55, 70)])
    yeast = DecimalField('Yeast %', description='Ingredient', validators=[InputRequired(), NumberRange(0, 3)])
    salt = DecimalField('Salt %', description='Ingredient', validators=[InputRequired(), NumberRange(0, 4)])
    oil = DecimalField('Oil %', description='Ingredient', validators=[Optional(), NumberRange(0, 8)])
    sugar = DecimalField('Sugar %', description='Ingredient', validators=[Optional(), NumberRange(0, 4)])
    submit = SubmitField('Send')

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            if not (self.dough_weight.data and self.g_oz.data or self.thickness_factor.data and self.pizza_size.data):
                return False
            else:
                return True

        return False
