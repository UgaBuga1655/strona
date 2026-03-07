from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FieldList, FormField, SearchField
from wtforms.validators import DataRequired, Length
from .models import Author

class SongSearchForm(FlaskForm):
    query = StringField(
        'Tytuł, autor', validators=[DataRequired(), 
        Length(min=3, max=100)], 
        render_kw={'placeholder' :'Tytuł, autor...'})
    submit = SubmitField('Wyszukaj')


class VerseForm(FlaskForm):
    class Meta:
        csrf = False  # no need to use CSRF here, since this is a sub-form
    text = TextAreaField('Tekst', validators=[DataRequired()])
    chords = TextAreaField('Akordy', validators=[DataRequired()])
    type_ = SelectField('Typ', choices=[
        ('v', 'Zwrotka'),
        ('c', 'Refren'),
        ('b', 'Most'),
    ])

class AuthorForm(FlaskForm):
    author = SelectField('Autor', choices=[], coerce=int)

class NewSongForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    authors = FieldList(FormField(AuthorForm), min_entries=1)
    verses = FieldList(FormField(VerseForm), min_entries=1)
    submit = SubmitField('Submit')