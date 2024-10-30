from flask import Blueprint, render_template, request, redirect, url_for
from forms import SongSearchForm
from models import Tag, Song, Author

spiewnik = Blueprint('spiewnik', __name__, )
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

@spiewnik.route('/song/<id>')
def song(id):
    song = Song.query.filter_by(id=id).first()
    return render_template("song.html", song=song, active_tab=active_tab)

@spiewnik.route('/author/<id>')
def author(id):
    author = Author.query.filter_by(id=id).first()
    songs = author.songs
    return render_template('search.html', results=songs, form=SongSearchForm(), query=author.name)

@spiewnik.route('/tag/<id>')
def tag(id):
    tag = Tag.query.filter_by(id=id).first()
    songs = tag.songs
    return render_template('search.html', results=songs, form=SongSearchForm(), query=tag.name)