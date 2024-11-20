from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField

class ViewSoldiersForm(FlaskForm):
    password = PasswordField('Hasło')
    submit = SubmitField('Zobacz żołnierzy')