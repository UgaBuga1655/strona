from flask import Blueprint, url_for, render_template, make_response, request
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
import os
from random import choice
from PIL import Image
from datetime import date

class DateForm(FlaskForm):
    date = DateField(label='Data')
    submit = SubmitField('Zgaduj')

gabaguessr = Blueprint('gabaguessr', __name__, template_folder='templates', static_folder='static')

def get_score(days):
    if days <= 3:
        return 1000
    if days <= 30:
        return 1000 - (days-3) * 18.5
    if days <= 150:
        return 400 - (days-30) * 3.7
    return 0


@gabaguessr.route('/')
def index():
    response = make_response()
    response.set_cookie('total_score', '0')
    response.set_cookie('stage', '0')
    response.set_data(render_template('guessr.html'))
    return response

@gabaguessr.route('/game', methods=['POST', 'GET'])
def game():
    response = make_response()

    # open random image
    files = os.listdir(gabaguessr.static_folder)
    image = choice(files)
    img = Image.open(gabaguessr.static_folder + '/' + image)

    # get date
    date_time = img.getexif().get(306, 'Unknown')
    display_date = '-'.join(date_time.split(' ')[0].split(':'))
    display_date = date.fromisoformat(display_date)

    # get stage
    stage = int(request.cookies.get('stage'))

    # create
    form = DateForm()
    if form.validate_on_submit():
        guess_date = form.date.data
        correct_date = date.fromisoformat(request.cookies.get('correct'))
        delta = guess_date-correct_date
        score = int(get_score(abs(delta.days)))
        total_score = int(request.cookies.get('total_score'))
        total_score += score
        response.set_cookie('total_score', str(total_score))
        
        response.set_data(render_template('score.html', guess_date=guess_date, correct_date=correct_date, score=score, total=total_score, over = stage>=5))
        return response

    # increment stage
    stage += 1
    response.set_cookie('stage', str(stage))
    
    response.set_data(render_template('game.html', image=url_for('.static', filename=image), date_time=display_date, form = form, stage=stage))
    response.set_cookie('correct', display_date.isoformat())
    return response

@gabaguessr.route('game_over')
def game_over():
    total = request.cookies.get('total_score')
    response = make_response(render_template('game_over.html', total=total))
    response.set_cookie('stage', '0')
    response.set_cookie('total_score', '0')
    return response
