from flask import Blueprint, render_template, request, redirect
from .forms import SongSearchForm, NewSongForm
from .models import Tag, Song, Author
from itertools import zip_longest

spiewnik = Blueprint('spiewnik', __name__, template_folder='templates', static_folder='static')
active_tab="spiewnik"

@spiewnik.route('/', methods=['GET', 'POST'])
def spiewnik_index():
    form = SongSearchForm()
    if request.method == 'GET':
        return render_template('spiewnik.html', tags=Tag.query.all(), form=form, active_tab=active_tab)
    
    # search for songs
    query = f'%{form.query.data}%'
    songs = Song.query.filter(Song.title.like(query)).order_by(Song.title).all()
    authors = Author.query.filter(Author.name.like(query)).order_by(Author.name).all()
    results = sorted(songs+authors, key = lambda x: x.Name())

    # if only one result redirect directly to it
    if len(results)==1:
        return redirect(results[0].Link())
    
    return render_template('search.html', results = results, form=form, active_tab=active_tab)

@spiewnik.route('/song/<int:id>')
def song(id):
    song = Song.query.filter_by(id=id).first()
    return render_template("song.html", song=song, active_tab=active_tab)

@spiewnik.route('/author/<int:id>')
def author(id):
    author = Author.query.filter_by(id=id).first()
    songs = author.songs
    songs.sort(key=lambda s: s.title)
    return render_template('search.html', results=songs, form=SongSearchForm(), query=author.name)

@spiewnik.route('/tag/<int:id>')
def tag(id):
    tag = Tag.query.filter_by(id=id).first()
    songs = tag.songs
    songs.sort(key=lambda s: s.title)
    return render_template('search.html', results=songs, form=SongSearchForm(), query=tag.name)

@spiewnik.route('/song/new', methods=['GET', 'POST'])
def create_song():
    authors = [(author.id, author.name) for author in Author.query.order_by(Author.name).all()]
    form = NewSongForm()
    form.authors.entries[0].author.choices = [(author.id, author.name) for author in Author.query.order_by(Author.name).all()]
    if form.validate_on_submit():
        print(f'Tytuł: {form.title.data}')
        authors = [Author.query.filter_by(id=a['author']).first().name for a in form.authors.data]
        print('Autor: ' + ','.join(authors))
        # print(f'Autorzy: {",".join(a["author"].data for a in form.authors.data)}')
        for verse in form.verses.data:
            indent = '    ' if verse['type_'] == 'c' else ''
            print(indent + verse['type_'])
            for text, chords in zip_longest(verse['text'].split('\n'), verse['chords'].split('\n')):
                print(f'{indent}{text}\t\t{chords}')
    else:
        print(form.errors)

    return render_template('new.html', form=form)