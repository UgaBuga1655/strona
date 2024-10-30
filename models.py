from db_config import db
from flask import url_for

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
    def Link(self):
        return url_for('spiewnik.song', id=self.id)
    

    def Name(self):
        title = self.title
        if len(self.authors) > 0:
            authors_names = [author.name for author in self.authors]
            title += " - " + ', '.join(authors_names)
        return title
    
    def verses_in_order(self):
        if self.verse_order == None:
            return self.verses
        
        verses_in_order = []
        for name in self.verse_order.split():
            verse = Verse.query.filter_by(song_id = self.id, name=name).first()
            verses_in_order.append(verse)
        return verses_in_order
    

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def Name(self):
        return self.name + ' (autor)'

    def Link(self):
        return url_for('spiewnik.author', id=self.id)

class Verse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    text = db.Column(db.Text, nullable=False)
    chords = db.Column(db.Text)

    def Indent_class(self):
        if 'c' in self.name:
            return 'chorus'
        return ''

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
