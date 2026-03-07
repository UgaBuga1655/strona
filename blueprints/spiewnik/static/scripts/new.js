function addVerse() {
    console.log('add verse')
        const firstVerse = document.querySelector('.verseField');
        const newVerse = document.createElement('div');
        newVerse.classList.add('verseField');
        newVerse.innerHTML = firstVerse.innerHTML;
        const newIndex = document.querySelectorAll('.verseField').length;
        const text = newVerse.querySelector('#verses-0-text');
        text.id = `verses-${newIndex}-text`;
        text.name = text.id;
        text.value = '';
        const type = newVerse.querySelector('#verses-0-type_');
        type.id = `verses-${newIndex}-type_`;
        type.name = type.id;
        type.value = 'v';
        const chords = newVerse.querySelector('#verses-0-chords');
        chords.id = `verses-${newIndex}-chords`;
        chords.name = chords.id;
        chords.value = '';
        document.getElementById('verseFields').appendChild(newVerse);
        document.querySelector('.verseField:last-child input').focus();
        return false;
      }