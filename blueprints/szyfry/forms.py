from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired

alphabets = [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ',
    'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
]

options_sylabowy = [
    "GADERYPOLUKI",
    "POLITYKARENU",
    "MOTYLECUDAKI",
    "KACEMINUTOWY",
    "KONIECMATURY",
    "NOWEBUTYLISA",
    "MALINOWEBUTY",
    "BITWAOCHMURY",
    "BAWOLETYKIJU",
    "ZIELONYBUK",
    "NASZHUFIEC",
    "GUBIKALESONY",
    "POLEMINEFAGU",
    "PADYGIMOZETU",
    "KULOPERYZAGI",
    "REGULAMINOWY",
    "HALOJUPITERY"
]


class DiacriticsForm(FlaskForm):
    message = TextAreaField(label='Wiadomość:', validators=[DataRequired()], render_kw={"placeholder": "Twoja wiadomość..."})
    submit = SubmitField('Potwierdź')

    def __init__(self, message):
        super().__init__()
        self.message.data = message


class CipherForm(FlaskForm):
    message = TextAreaField(label='Wiadomość:', validators=[DataRequired()], render_kw={"placeholder": "Twoja wiadomość..."})
    submit = SubmitField('Potwierdź')
    mode = SelectField(label='Tryb:', choices=['Zaszyfruj', 'Odszyfruj'])

    def __init__(self, message=None):
        super().__init__()
        if message is not None:
            self.message.data = message


class CezarForm(CipherForm):
    alphabet = SelectField(label='Alfabet:', choices=alphabets)
    move = IntegerField(label='Przesunięcie:', default=3)

    # def __init__(self, message):
    #     super().__init__(message)
    #     self.message.data = message


class VigenereForm(CipherForm):
    key = TextAreaField(label='Klucz:', render_kw={"placeholder": "Pozostaw pusty, aby wygenerować losowy"})
    alphabet = SelectField(label='Alfabet:', choices=alphabets)

    # def __init__(self, message):
    #     super().__init__(message)
    #     self.message.data = message


class SylabowyForm(CipherForm):
    mode = SelectField(label='Szyfr: ', choices=options_sylabowy)

    # def __init__(self, message):
    #     super().__init__(message)
    #     self.message.data = message
