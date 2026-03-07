from flask import Blueprint, redirect, url_for, render_template, make_response, request
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
import os
from random import choice, shuffle
from PIL import Image
from datetime import date

from wtforms.validators import DataRequired

class DateForm(FlaskForm):
    date = DateField(label='Data', validators=[DataRequired()])
    submit = SubmitField('Zgaduj')

gabaguessr = Blueprint('gabaguessr', __name__, template_folder='templates', static_folder='static')

SCORES = [
    (-1, 1000),
    (3, 1000),
    (7, 950),
    (14, 800),
    (31, 650),
    (61, 500),
    (100, 250),
    (150, 0)
]

def get_score(days):
    days = abs(days)
    for n, pair in enumerate(SCORES):
        if days <= pair[0]:
            xa, ya = SCORES[n-1]
            xb, yb = SCORES[n]
            return int((yb-ya)*(days-xa)/(xb-xa)+ya)
    return 0

def reset_game(response):
    response.set_cookie('total_score', '0')
    response.set_cookie('stage', '1')
    files = os.listdir(gabaguessr.static_folder)
    shuffle(files)
    images = files[0:5]
    response.set_cookie('images', ';'.join(images))
    return response

@gabaguessr.route('/')
def index():
    response = make_response()
    reset_game(response)
    response.set_data(render_template('guessr.html'))
    return response

@gabaguessr.route('/game', methods=['POST', 'GET'])
def game():
    response = make_response()

    # get stage
    stage = request.cookies.get('stage')
    if stage:
        stage = int(stage)
    else:
        response = make_response(redirect(url_for('gabaguessr.game')))
        reset_game(response)
        return response

    form = DateForm()
    if form.validate_on_submit():
        guess_date = form.date.data
        correct_date = date.fromisoformat(request.cookies.get('correct'))
        delta = guess_date-correct_date
        days = abs(delta.days)
        score = int(get_score(days))

        total_score = int(request.cookies.get('total_score'))
        total_score += score
        response.set_cookie('total_score', str(total_score))

        if days == 0:
            message = choice(['Brawo, to był dokładnie ten dzień! 😍',
                              'WOW, to właśnie wtedy! 😯'])
        elif days <= 3:
            message = 'Udało się! Pomyliłaś się tylko o kilka dni! 😎'
        elif days <= 31:
            message = choice(['Nieźle, walnęłaś się ledwie o parę tygoni. 👍',
                              'Całkiem nieźle. 😘',
                              'Trafiłaś w dobry miesiąc! 🥳'])
        elif days <= 150:
            message = choice(['To nawet nie ten miesiąc... 😐',
                              'Przynajmniej dobre półrocze... 😔'])
        else:
            message = 'Oj baka, to zdecydowanie nie wtedy! 😭😭😭'

        bar_style = f'style=width:{int(total_score/50)}%;background-color:#e33bea' 
        response.set_data(render_template('score.html', guess_date=guess_date, score=score, \
                                          total=total_score, over = stage>=5, bar_style=bar_style,\
                                            message=message))
        # increment stage
        stage += 1
        if stage > 5:
            stage = 5
        response.set_cookie('stage', str(stage))
        return response

    # get the right image
    image = request.cookies.get('images').split(';')[stage-1]
    img = Image.open(gabaguessr.static_folder + '/' + image)

    # get date
    date_time = img.getexif().get(306, 'Unknown')
    display_date = '-'.join(date_time.split(' ')[0].split(':'))
    display_date = date.fromisoformat(display_date)

    
    response.set_data(render_template('game.html', image=url_for('.static', filename=image), date_time=display_date, form = form, stage=stage))
    response.set_cookie('correct', display_date.isoformat())
    return response

@gabaguessr.route('game_over')
def game_over():
    total = int(request.cookies.get('total_score'))
    images = request.cookies.get('images').split(';')
    images = [url_for('.static', filename=image) for image in images]

    bar_style = f'style=width:{int(int(total)/50)}%;background-color:#e33bea' 
    response = make_response(render_template('game_over.html', total=total, images=images, bar_style=bar_style))
    return response

@gabaguessr.route('restart')
def restart():
    response = make_response(redirect(url_for('gabaguessr.game')))
    reset_game(response)
    # response.set_data(redirect(url_for('gabaguessr.game')))
    return response

