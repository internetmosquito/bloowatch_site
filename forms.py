__author__ = 'mosquito'

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[DataRequired(),
        Email(),
        Length(min=6, max=40)]
    )
