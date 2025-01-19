from flask_wtf import FlaskForm
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


class CipherForm(FlaskForm):
    message = TextAreaField(label='Wiadomość:', validators=[DataRequired()], render_kw={"placeholder": "Twoja wiadomość..."})
    submit = SubmitField('Potwierdź')
    mode = SelectField(label='Tryb:', choices=['Zaszyfruj', 'Odszyfruj'])


class CezarForm(CipherForm):
    alphabet = SelectField(label='Alfabet:', choices=alphabets)
    move = IntegerField(label='Przesunięcie:', default=3)


class VigenereForm(CipherForm):
    key = TextAreaField(label='Klucz:', render_kw={"placeholder": "Pozostaw pusty, aby wygenerować losowy"})
    alphabet = SelectField(label='Alfabet:', choices=alphabets)


class SylabowyForm(CipherForm):
    mode = SelectField(label='Szyfr: ', choices=options_sylabowy)
