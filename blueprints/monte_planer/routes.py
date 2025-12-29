from flask import Blueprint, render_template

monte_planer = Blueprint('monte_planer', __name__, template_folder='templates', static_folder='static')
active_tab = 'monte_planer'

@monte_planer.route('/')
def planer_index():
    return render_template('monte_planer.html', active_tab=active_tab)