from flask import Blueprint, render_template, request
import json
import re

def morse_encrypt(text):
    morse = {
        'a' : '·–',
        'ą' : '·–',
        'b' : '–···',
        'c' : '–·–·',
        'ć' : '–·–·',
        'd' : '–··',
        'e' : '·',
        'ę' : '·',
        'f' : '··–·',
        'g' : '––·',
        'h' : '····',
        'i' : '··',
        'j' : '·–––',
        'k' : '–·–',
        'l' : '·–··',
        'ł' : '·–··',
        'm' : '––',
        'n' : '–·',
        'ń' : '–·',
        'o' : '–––',
        'ó' : '–––',
        'p' : '·––·',
        'r' : '·–·',
        's' : '···',
        'ś' : '···',
        't' : '–',
        'u' : '··–',
        'v' : '···–',
        'w' : '·––',
        'x' : '–··–',
        'y' : '–·––',
        'z' : '––··',
        'ź' : '––··',
        'ż' : '––··',
        '1' : '·––––',
        '2' : '··–––',
        '3' : '···––',
        '4' : '····–',
        '5' : '·····',
        '6' : '–····',
        '7' : '––···',
        '8' : '–––··',
        '9' : '––––·',
        '0' : '–––––',
        '.' : '',
        '!' : '',
        '?' : '',
        ' ' : ''
    }
    text = text.lower()
    response = ''
    for letter in text:
        try:
            response += morse[letter]+"/"
        except:
            pass
    return response

def morse_decrypt(message):
    morse = {
        '///' : '.',
        '//' : ' ',
        '·––––' : '1',
        '··–––' : '2',
        '···––' : '3',
        '····–' : '4',
        '·····' : '5',
        '–····' : '6',
        '––···' : '7',
        '–––··' : '8',
        '––––·' : '9',
        '–––––' : '0',
        '–··–' : 'x',
        '–·––' : 'y',
        '––··' : 'z',
        '···–' : 'v',
        '–···' : 'b',
        '–·–·' : 'c',
        '··–·' : 'f',
        '·–––' : 'j',
        '····' : 'h',
        '·–··' : 'l', 
        '·––·' : 'p',
        '–··' : 'd',
        '––·' : 'g',
        '–·–' : 'k',
        '·–·' : 'r',
        '···' : 's',
        '·––' : 'w',
        '–––' : 'o',
        '··–' : 'u',
        '·–' : 'a',
        '··' : 'i',
        '––' : 'm',
        '–·' : 'n',
        '–' : 't',
        '·' : 'e',
        '/' : ''
    }
    message = message.replace('.', '·').replace('-', '–')

    for symbol in morse.keys():
        message = message.replace(symbol, morse[symbol])

    return message



szyfry = Blueprint('szyfry', __name__, )
# cors = CORS(szyfry, resources={r"/*": {"origins": "*"}})
active_tab="szyfry"

@szyfry.route("/")
def index():
    return render_template("szyfry.html", active_tab=active_tab)

@szyfry.route("/morse", methods=["POST"])
def morse():
    
    message = request.get_json()
    print(message)


    # print(message)s
    message = morse_encrypt(message["text"]) if message['mode']=='zaszyfruj' else morse_decrypt(message['text'])
    response = json.dumps(message)

    # print(response)
    return response