from flask import Blueprint, render_template
from unidecode import unidecode
from .forms import CezarForm, CipherForm, VigenereForm, SylabowyForm, DiacriticsForm
from .functions import morse_process, cezar_process, vigenere_process, sylabowy_process


szyfry = Blueprint('szyfry', __name__, template_folder='templates', static_folder='static')
active_tab = "szyfry"


@szyfry.route("/")
def index():
    return render_template("szyfry.html", active_tab=active_tab)


@szyfry.route("/morse", methods=["GET", "POST"])
def morse():
    form = CipherForm()
    message = None
    if form.validate_on_submit():
        message = morse_process(form)
    return render_template("morse.html", active_tab=active_tab, form=form, message=message)


@szyfry.route("/cezar", methods=["GET", "POST"])
def cezar():
    form = CezarForm()
    message = None
    if form.validate_on_submit():
        message = cezar_process(form)
    return render_template("cezar.html", active_tab=active_tab, form=form, message=message)


@szyfry.route("/vigenere", methods=["GET", "POST"])
def vigenere():
    form = VigenereForm()
    message = None
    if form.validate_on_submit():
        message, form.key.data = vigenere_process(form)
    return render_template("vigenere.html", active_tab=active_tab, form=form, message=message)


@szyfry.route("/sylabowy", methods=["GET", "POST"])
def sylabowy():
    form = SylabowyForm()
    message = None
    if form.validate_on_submit():
        message = sylabowy_process(form)
    return render_template("sylabowy.html", active_tab=active_tab, form=form, message=message)


@szyfry.route("/remove-diacritics", methods=["GET", "POST"])
def diacritics():
    form = DiacriticsForm()
    message = None
    if form.validate_on_submit():
        message = unidecode(form.message.data)
    return render_template("diacritics.html", active_tab=active_tab, form=form, message=message)
