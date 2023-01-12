const inputFile = document.getElementById("file-form")

inputFile.onchange = (e) => {
    const file = inputFile.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (e) => {
        textContent = e.target.result
        let text_field = document.getElementById("text-field")
        text_field.innerHTML = textContent
        document.getElementById("form").submit();
        // console.log(`The content of ${file.name} is \n${textContent}`)
    }
    reader.onerror = (e) => {
        const error = e.target.error
        console.error(`Error occured while reading ${file.name}`, error)
    }
    reader.readAsText(file)
}

function saveAnswers() {
    response = document.getElementById("answers").innerHTML.replace(/^\s*\n?|<br>/gm, "")
    if (response == "") { return false }
    var myFile = new File([response], "odpowiedzi.txt", {type: "text/plain;charset=utf-8"});
    saveAs(myFile);
}