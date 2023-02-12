function markTab(tab) {
    let last = document.getElementById("select").getElementsByClassName("active-tab");
    if (last.length>0){
        last[0].classList.remove("active-tab")
    }
    tab.classList.add("active-tab")
}

function clearInputCard() {
    let current = document.getElementById("input").getElementsByClassName("visible");
    if (current.length>0){
        current[0].classList.remove("visible")
    }
}

function populateInputCard(tab, szyfr) {
    markTab(tab)
    clearInputCard()
    document.getElementById(szyfr).classList.add("visible");
}

function processMorse() {
    let message = document.getElementById("morse-message").value
    if (message == '') {
        return false
    }
    let mode = document.getElementById("morse-mode").value
    fetch("/szyfry/morse", {
        "body": JSON.stringify({"text" : message, "mode" : mode}),
        "headers" : {"Content-Type" : "application/json"},
        "method": "POST"
    })
    .then((res) => {
        return res.json()
    })
    .then(
        data => {
            console.log(data)
            let response_card = document.getElementById('morse-response');
            response_card.innerHTML = data
            response_card.classList.remove('invisible')
        }
    )
    .catch((err) => console.log(err))
}

function processCezar() {
    let message = document.getElementById("cezar-message").value
    if (message == '') {return false}
    let alphabet = document.getElementById("cezar-alphabet").value
    let mode = document.getElementById("cezar-mode").value
    let move = document.getElementById("cezar-move").value
    fetch("/szyfry/cezar", {
        "body": JSON.stringify({"text" : message, "alphabet": alphabet, "mode" : mode, "move" : move}),
        "headers" : {"Content-Type" : "application/json"},
        "method": "POST"
    })
    .then((res) => {
        return res.json()
    })
    .then(
        data => {
            console.log(data)
            let response_card = document.getElementById('cezar-response');
            response_card.innerHTML = data
            response_card.classList.remove('invisible')
        }
    )
    .catch((err) => console.log(err))
}

function processSylabowy() {
    let message = document.getElementById("sylabowy-message").value
    if (message == '') {return false}
    let key = document.getElementById("sylabowy-key").value
    fetch("/szyfry/sylabowy", {
        "body": JSON.stringify({"text" : message, "key": key}),
        "headers" : {"Content-Type" : "application/json"},
        "method": "POST"
    })
    .then((res) => {
        return res.json()
    })
    .then(
        data => {
            console.log(data)
            let response_card = document.getElementById('sylabowy-response');
            response_card.innerHTML = data
            response_card.classList.remove('invisible')
        }
    )
    .catch((err) => console.log(err))
}
