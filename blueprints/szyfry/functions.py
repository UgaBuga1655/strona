from random import randint


def morse_encrypt(text):
    morse = {
        'a': '·–',
        'ą': '·–',
        'b': '–···',
        'c': '–·–·',
        'ć': '–·–·',
        'd': '–··',
        'e': '·',
        'ę': '·',
        'f': '··–·',
        'g': '––·',
        'h': '····',
        'i': '··',
        'j': '·–––',
        'k': '–·–',
        'l': '·–··',
        'ł': '·–··',
        'm': '––',
        'n': '–·',
        'ń': '–·',
        'o': '–––',
        'ó': '–––',
        'p': '·––·',
        'r': '·–·',
        's': '···',
        'ś': '···',
        't': '–',
        'u': '··–',
        'v': '···–',
        'w': '·––',
        'x': '–··–',
        'y': '–·––',
        'z': '––··',
        'ź': '––··',
        'ż': '––··',
        '1': '·––––',
        '2': '··–––',
        '3': '···––',
        '4': '····–',
        '5': '·····',
        '6': '–····',
        '7': '––···',
        '8': '–––··',
        '9': '––––·',
        '0': '–––––',
        '.': '/',
        '!': '/',
        '?': '/',
        ' ': ''
    }
    text = text.lower()
    response = ''
    for letter in text:
        try:
            response += morse[letter]+"/"
        except (Exception):
            response += ''
    return response


def morse_decrypt(message):
    morse = {
        '///': '.',
        '//': ' ',
        '·––––': '1',
        '··–––': '2',
        '···––': '3',
        '····–': '4',
        '·····': '5',
        '–····': '6',
        '––···': '7',
        '–––··': '8',
        '––––·': '9',
        '–––––': '0',
        '–··–': 'x',
        '–·––': 'y',
        '––··': 'z',
        '···–': 'v',
        '–···': 'b',
        '–·–·': 'c',
        '··–·': 'f',
        '·–––': 'j',
        '····': 'h',
        '·–··': 'l',
        '·––·': 'p',
        '–··': 'd',
        '––·': 'g',
        '–·–': 'k',
        '·–·': 'r',
        '···': 's',
        '·––': 'w',
        '–––': 'o',
        '··–': 'u',
        '·–': 'a',
        '··': 'i',
        '––': 'm',
        '–·': 'n',
        '–': 't',
        '·': 'e',
        '/': ''
    }
    message = message.replace('.', '·').replace('-', '–')

    for symbol in morse.keys():
        message = message.replace(symbol, morse[symbol])

    return message


def morse_process(form):
    if form.mode.data == 'Zaszyfruj':
        return morse_encrypt(form.message.data)
    return morse_decrypt(form.message.data)


def cezar_process(form):
    response = ''
    text = form.message.data
    upper = form.alphabet.data
    lower = upper.lower()
    mode = 1 if form.mode.data == 'Zaszyfruj' else -1
    move = form.move.data % len(upper)
    for letter in text:
        if letter in upper:
            i = upper.index(letter)
            response += upper[(i+mode*move) % len(upper)]
        elif letter in lower:
            i = lower.index(letter)
            response += lower[(i+mode*move) % len(lower)]
        else:
            response += letter
    return response


def sylabowy_process(form):
    response = ''
    text = form.message.data
    key = form.mode.data+form.mode.data.lower()
    for letter in text:
        if letter in key:
            i = key.index(letter)
            letter = (key[i-1] if i % 2 else key[i+1])
        response += letter
    return response


def vigenere_process(form):
    message = ''
    text = form.message.data
    upper = form.alphabet.data
    lower = upper.lower()
    al_len = len(upper)
    rawkey = form.key.data.upper()

    # formatuje klucz, żeby to były same duże litery
    if rawkey:
        key = [x for x in rawkey if x in upper]
    else:
        # liczy znaki w tekście, które należa do alfabetu
        condensed_text = [x for x in text.upper() if x in upper]
        # losuje literę klucza dla każdej litery w skondensowanym tekście
        key = [upper[randint(1, al_len)-1] for _ in condensed_text]

    key_len = len(key)
    mode = 1 if form.mode.data == 'Zaszyfruj' else -1
    k = 0
    for letter in text:
        if letter in upper:
            # numer litery w wiadomości
            i = upper.index(letter)
            # przesunięcie to numer odpowiedniej litery klucza
            move = upper.index(key[k % key_len])
            # stosuje szyfr cezara z właściwym przesunięciem
            message += upper[(i + move * mode) % al_len]
            k += 1
        elif letter in lower:
            i = lower.index(letter)
            move = upper.index(key[k % key_len])
            message += lower[(i + move * mode) % al_len]
            k += 1
        else:
            message += letter
    return message, ''.join(key)
