from db_config import db

song_author = db.Table('song_author',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

song_tag = db.Table('song_tag',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    authors = db.relationship('Author', secondary=song_author, backref='songs')
    verse_order = db.Column(db.String(150))
    verses = db.relationship('Verse', backref='song')
    tags = db.relationship('Tag', secondary=song_tag, backref='songs')

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

class Verse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    text = db.Column(db.Text, nullable=False)
    chords = db.Column(db.Text)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
