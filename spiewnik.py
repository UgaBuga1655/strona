from BaseXClient import BaseXClient
from flask import Blueprint, render_template, request, redirect
from markupsafe import escape
import xml.etree.ElementTree as ET
import re
import os

def start_session():
    # HACK YOLO
    with open("./passwd")as file:
        passwd = file.read().strip()
    while True:
        try:
            session = BaseXClient.Session('localhost', 1984, 'admin', passwd)
            break
        except:
            os.system("basexserver -S")
            
    return session

def setup():
    session = start_session()

    try:
        # create new database
        if "songs" in session.execute("list"):
            print("Refreshing current database...")
            session.execute("drop db songs")

        session.execute("create db songs ./songs")

        # print(session.execute("xquery song[properties/titles/title[contains(. ,'Zmartwychwstał')]]"))

        print("Database loaded successfully!")
    finally:
        # close session
        if session:
            session.close()


def serialize_node_group(group):
    return [element.text for element in group]

def render_html(song):
    html = {}
    song = ET.fromstring(song)

    # tytuł
    titles = song.findall("./properties/titles/title")
    html["first_title"] = titles.pop(0).text
    html["secondary_titles"] = serialize_node_group(titles)

    # autorzy
    authors = song.findall("./properties/authors/author")
    authors = serialize_node_group(authors)
    try:   
        if authors[0] == None or authors[0] == "()":
            html["authors"] = ""
        else:
            html["authors"] = authors 
    except:
        html["authors"] = ""

    # kolejność zwrotek
    verse_order = song.find("./properties/verseOrder")

    try:
        verse_order = verse_order.text.split(' ')
    except:
        verse_order = []
        for verse in song.findall("./lyrics/"):
            verse_order.append(verse.attrib['name'])


    # tekst
    html["verses"] = []
    for verse_name in verse_order:
        # znalezienie zwrotki i zamiana na stringa
        verse_text = song.find(f"./lyrics/verse[@name='{verse_name}']/lines")
        verse_text  = ET.tostring(verse_text, encoding='unicode')
        # dzielenie na linijki
        verse_text = re.sub('</*lines>', '', verse_text)
        verse_text = verse_text.strip().split("<br />")
        verse = {}
        verse["text"] = verse_text
        # wcięcie dla nie-zwrotek
        if not re.match("v", verse_name):
            verse["class"] = "indent"
        html["verses"].append(verse)

    # tagi
    themes = song.findall("./properties/themes/theme")
    html["themes"] = serialize_node_group(themes)


    
    return html


spiewnik = Blueprint('spiewnik', __name__, )
active_tab="spiewnik"

@spiewnik.route('/')
def spiewnik_index():
    themes = [
        'Maryjne', 'Religijne', 'Patriotyczne', 'Ludowe', 'Harcerskie', 'Bożonarodzeniowe'
    ]
    themes.sort()
    return render_template("spiewnik.html", themes=themes, active_tab=active_tab)

@spiewnik.route('/search/<title>', methods=["POST", "GET"])
def search_song(title):
    
    title = escape(title)
    session = start_session()
    try:
        session.execute("open songs")
        query = f"xquery for $x in song/properties \
                let $title := $x/titles/title[matches(upper-case(.), upper-case('{title}'))] \
                where $title or $x/authors/author[matches(upper-case(.), upper-case('{title}'))] \
                return concat(\
                    if (count($title)=1) then ( \
                        data($title) \
                    ) else ( \
                        data($x/titles/title[1]) \
                    ), \
                    if ($x/authors/author) then (\
                        concat(' - ', string-join(($x/authors/author), ', '))\
                    ) else (''))"

        
                # znajduje piosenki, które mają tytuł lub autora zgodnego z wynikiem wyszukuwania
                # bierze dopasowany tytuł, jeśli jest dokładnie jeden
                # bierze pierwszy tytuł jeśli są więcej niż jeden dopasowane tytuły lub żaden (piosenka została dopasowana po autorze)
                # dopisuje autora, jeśli piosenka go ma

        titles = session.execute(query).split("\n")
        titles.sort()

    finally:
        if session:
            session.close()


    # redirect directly to the song if only one matches the search term
    if len(titles)==1:
        return redirect(f"/spiewnik/song/{titles[0].split(' - ')[0]}")
    
    if request.method == "POST":
        return titles
    else:
        return render_template("search.html", titles=titles, active_tab=active_tab)
    

@spiewnik.route('/song/<title>')
def show_song(title):
    title = escape(title)
    session = start_session()
    try:
        session.execute("open songs")
        song = session.execute(f'xquery song[properties/titles[title = "{title}"]]')
    finally:
        if session:
            session.close()

    if not song:
            return "Nie znaleziono takiego utworu..."

    return render_template("song.html", song=render_html(song), title=title, active_tab=active_tab)
    
@spiewnik.route('/download/<title>')
def download_song(title):
    title = escape(title)
    session = start_session()
    try:
        session.execute("open songs")
        song = session.execute(f'xquery song[properties/titles[title = "{title}"]]')
    finally:
        if session:
            session.close()

    # o co biega? Kiedy atrybut xmlns z jakiegoś powodu totalnie wykrzacza BaseX, a bez niego wykrzacza się OpenLP, dlatego w bazie danych pliki go nie mają, a jest dodawany przy pobieraniu... 😒
    # HACK
    song = ET.fromstring(song)
    song.set("xmlns", "http://openlyrics.info/namespace/2009/song")
    song = ET.tostring(song, encoding='unicode')

    return song

@spiewnik.route('/author/<name>')
def author(name):
    name = escape(name)
    session = start_session()
    try:
        session.execute("open songs")
        query = f"xquery for $x in song/properties[authors/author='{name}']\
                order by $x/titles/*[1] \
                return concat(data($x/titles/*[1]), ' - ', string-join(($x/authors/author), ', '))"
        titles = session.execute(query).split("\n")
    finally:
        if session:
            session.close()

    return render_template("search.html", titles=titles, author=name, active_tab=active_tab)

@spiewnik.route('/theme/<theme>')
def theme(theme):
    theme = escape(theme)
    session = start_session()
    try:
        session.execute("open songs")
        query = f"xquery for $x in song/properties[themes/theme='{theme}'] \
                let $title := $x/titles/*[1]\
                order by $title \
                return concat( \
                    data($title), \
                    if(($x/authors/author)) then ( \
                        concat(' - ', string-join(($x/authors/author), ', ')) \
                    ) else () )"

        print(query)
        titles = session.execute(query).split("\n")
    finally:
        if session:
            session.close()

    return render_template("search.html", titles=titles, author=theme, active_tab=active_tab)