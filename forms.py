from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subj = StringField('Subject', validators=[DataRequired(), Length(max=70)])
    msg = TextAreaField('Message', validators=[DataRequired()])
    honey = StringField('Website', validators=[Optional()])
    submit = SubmitField('Send')
