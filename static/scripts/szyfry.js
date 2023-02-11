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
