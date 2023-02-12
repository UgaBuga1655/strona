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
        '.' : '/',
        '!' : '/',
        '?' : '/',
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

def cezar_encrypt(message):
    response = ''
    text = message['text']
    upper = message["alphabet"]
    lower = upper.lower()
    mode = int(message['mode'])
    move = int(message['move'])%len(upper)
    for letter in text:
        if letter in upper:
            i = upper.index(letter)
            response += upper[(i+mode*move)%len(upper)]
        elif letter in lower:
            i = lower.index(letter)
            response += lower[(i+mode*move)%len(lower)]
        else:
            response += letter
    return response

def sylabowy_encrypt(message):
    response = ''
    text = message['text']
    key = message['key']+message['key'].lower()
    for letter in text:
        if letter in key:
            i = key.index(letter)
            letter = (key[i-1] if i%2 else key[i+1])
        response+=letter
    return response


szyfry = Blueprint('szyfry', __name__, )
active_tab="szyfry"

@szyfry.route("/")
def index():
    return render_template("szyfry.html", active_tab=active_tab)

@szyfry.route("/morse", methods=["POST"])
def morse():
    
    message = request.get_json()
    # print(message)


    # print(message)s
    message = morse_encrypt(message["text"]) if message['mode']=='zaszyfruj' else morse_decrypt(message['text'])
    response = json.dumps(message)

    # print(response)
    return response

@szyfry.route("/cezar", methods=["POST"])
def cezar():
    message = request.get_json()
    message = cezar_encrypt(message)
    response = json.dumps(message)
    return response

@szyfry.route("/sylabowy", methods=["POST"])
def sylabowy():
    message = request.get_json()
    message = sylabowy_encrypt(message)
    response = json.dumps(message)
    return response