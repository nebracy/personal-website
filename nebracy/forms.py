from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=75)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    subj = StringField('Subject', validators=[DataRequired(), Length(max=75)])
    msg = TextAreaField('Message', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Send')
    recaptcha = RecaptchaField()
