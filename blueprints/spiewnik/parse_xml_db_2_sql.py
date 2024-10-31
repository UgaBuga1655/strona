from app import app, db
import xml.etree.ElementTree as ET
import os
from blueprints.spiewnik.models import *

folder = 'songs'

with app.app_context():
    db.drop_all()
    db.create_all()
    for file in os.listdir(folder):
        file = folder + '/' + file
        with open(file) as f:
            content = f.read().strip().replace('\n', '').replace('\r', '')
            root = ET.fromstring(content)
        root


        properties = root.find('properties')

        # find title and create an object
        title = properties.find('titles/title').text
        song = Song(title=title)
        db.session.add(song)

        # Authors
        author_names = [author.text for author in properties.find('authors') if author.text is not None]

        for name in author_names:
            author = Author.query.filter_by(name = name).first()
            if author == None:
                author = Author(name=name)
                db.session.add(author)
            song.authors.append(author)
                
        # Tags
        themes = properties.find('themes')
        if themes != None:
            themes = [theme.text for theme in themes]
       
            for theme in themes:
                tag = Tag.query.filter_by(name=theme).first()
                if tag == None:
                    tag = Tag(name=theme)
                    db.session.add(tag)
                song.tags.append(tag)


        # Verse order
        verse_order = properties.find('verseOrder')
        if verse_order != None:
            verse_order = verse_order.text

        song.verse_order = verse_order



        print('Tytuł: ' + title)
        print('Autor: ' + ', '.join([author.name for author in song.authors]))
        print('Tagi:  ' + ', '.join([tag.name for tag in song.tags]))
        print('Kolejność zwrotek:', song.verse_order)

        # Lyrics <3
        lyrics = root.find('lyrics')

        verses = lyrics.findall('verse')
        for verse in verses:
            name = verse.get('name')
            lines = '\n'.join(verse.find('lines').itertext())
            verse = Verse(name=name, text=lines)
            song.verses.append(verse)

        for verse in song.verses:
            print(verse.name)
            print(verse.text)


        
        print('-----')


    db.session.commit()

    