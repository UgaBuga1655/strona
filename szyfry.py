from flask import Blueprint, render_template, request
import json
from random import randint

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

def vigenere_encrypt(message):
    response = {"text": '', "key" : ''}
    text = message['text']
    upper = message['alphabet']
    lower = upper.lower()
    al_len = len(upper)
    rawkey = message['key'].upper()

    # formatuje klucz, żeby to były same duże litery
    if rawkey:
        key = [x for x in rawkey if x in upper]
    else:
        # liczy znaki w tekście, które należa do alfabetu
        condensed_text = [x for x in text.upper() if x in upper]
        # losuje literę klucza dla każdej litery w skondensowanym tekście
        key = [upper[randint(1, al_len)-1] for _ in condensed_text]

    key_len = len(key)
    mode = int(message['mode'])
    k = 0
    for letter in text:
        if letter in upper:
            # numer litery w wiadomości
            i = upper.index(letter)
            # przesunięcie to numer odpowiedniej litery klucza
            move = upper.index(key[k%key_len])
            # stosuje szyfr cezara z właściwym przesunięciem
            response['text'] += upper[(i+move*mode)%al_len]
            k+=1
        elif letter in lower:
            i = lower.index(letter)
            move = upper.index(key[k%key_len])
            response['text'] += lower[(i+move*mode)%al_len]
            k+=1
        else:
            response['text'] += letter
    response['key'] = ''.join(key)
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

@szyfry.route("/vigenere", methods=["POST"])
def vigenere():
    message = request.get_json()
    message = vigenere_encrypt(message)
    response = json.dumps(message)
    return response