from flask import Blueprint, render_template
from .forms import ViewSoldiersForm


scouting = Blueprint('scouting', __name__, template_folder='templates', static_folder='static')
budynki = [
    ['Tartak', 0, 0, 0, 0],
    ['Kopalnia', 0, 0, 0, 0],
    ['Kamieniołom', 0, 0, 0, 0],
    ['Mennica', 0, 0, 0, 0],
    ['Koszary', 0, 0, 2, 0],
    ['Uniwersytet', 0, 0, 0, 0],
    ['Port', 0, 0, 0, 0],
    ['Zamek', 0, 0, 0, 0],
]

zasoby = {
    'Sokół' : {
        'D': 3, 'K' : 4, 'Ż': 1, 'Z' : 0
    },
    'Orzeł' : {
        'D': 0, 'K' : 2, 'Ż': 0, 'Z' : 0
    }
}


@scouting.route('/gra', methods=['GET', 'POST'])
def gra():
    form = ViewSoldiersForm()
    if form.validate_on_submit():
        print(form.password.data)
        if form.password.data == 'Oclaf':
            return render_template('gra.html', active_tab="gra",
                                   budynki=budynki, form=form, 
                                   view='sokół', zasoby=zasoby['Sokół'])
        if form.password.data == 'Aliuqa':
            return render_template('gra.html', active_tab="gra",
                                   budynki=budynki, form=form, 
                                   view='orzeł', zasoby=zasoby['Orzeł'])
    return render_template('gra.html', active_tab="gra", budynki=budynki, form = form)