from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SongSearchForm(FlaskForm):
    query = StringField(
        'Tytuł, autor', validators=[DataRequired(), 
        Length(min=3, max=100)], 
        render_kw={'placeholder' :'Tytuł, autor...'})
    submit = SubmitField('Wyszukaj')