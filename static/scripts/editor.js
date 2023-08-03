function checkIfStudentInTable(name, surname){
    table = document.getElementById("table")
    for (const row of table.children){
        if(row.querySelector("#name").innerHTML==name 
        && row.querySelector("#surname").innerHTML==surname){
            return true
        }
    };
    return false
}

function generateGroupLi(group_list, group) {
    li = document.createElement("button")
    li.setAttribute("onclick", "removeGroup(this)")
    li.setAttribute("id", group)
    li.innerHTML = group
    group_list.appendChild(li)
}

function addGroup(){
    let group_list = document.getElementById("groups")
    let group = document.getElementById("group-form").value

    if (group.trim() == ""){
        return false
    }

    // jeśli taki przedmiot już istnieje, to nic nie rób
    for (const list_element of group_list.children){
        if (list_element.innerHTML == group){
            return false
        }
    }
    
    generateGroupLi(group_list, group)

    // zaktualizuj aktywne pola wyboru
    for (const row of table.children){
        for (const td of row.children){
            if (td.id=="select"){
                updateSelection(td)
            }
        }
    }
    
    return true
}

function removeGroup(group){
    // usuwa przedmiot z listy i z tabeli
    let group_name = group.id
    let table = document.getElementById("table")
    group.remove()
    for (const row of table.children){
        for (const td of row.children){
            // usuwa pola z usuwanym przedmiotem
            if (td.id=="group-field" && td.innerHTML == group_name){
                td.remove()
            }
            // aktualizuje pola z selekcją
            if (td.id=="select"){
                updateSelection(td)
            }
        }
    }
}

function updateSelection(select){
    select.innerHTML = "" // usuwa obecne opcje
    let groups = document.getElementById("groups") // znajduje obecną listę możliwych rozszerzeń
    let row = select.parentElement

    // robi listę przedmiotów, które uczeń już rozszerza
    let current_groups = []
    for (const td of row.children){
        if (td.id == "group-field"){
            current_groups.push(td.innerHTML)
        }
    }

    // dodaje opcję dla każdego możliwego przedmiotu, o ile uczeń już go nie rozszerza
    for (const list_element of groups.children){
        if (!(current_groups.includes(list_element.id))){
            let option = document.createElement("option")
            option.innerHTML = list_element.id
            select.appendChild(option) 
        }

    }
}

function generateGroupSelect(element){
    // dodaje do rzędu pole do wyboru przedmiotu
    let select = document.createElement("select")
    select.setAttribute("id", "select")
    element.appendChild(select)
    updateSelection(select)
}

function generateConfirmButton(row){
    // dodaje do rzędu guzik do zatwierdzenia wyboru przedmiotu
    let confirm_button = document.createElement("button")
    confirm_button.innerHTML = "OK"
    confirm_button.setAttribute("id", "confirm_button")
    confirm_button.setAttribute("onclick", "confirmGroup(this.parentElement)")
    row.appendChild(confirm_button)
}

function confirmGroup(row){
    // przypisuje przedmiot uczniowi
    
    // dodaje pole z przedmiotem, o ile pole wyboru ma jakąś wartość
    select = row.querySelector("#select")
    let value = select.value
    if (value!=""){
        let group = document.createElement("button")
        group.setAttribute("id", "group-field")
        group.setAttribute("onclick", "removeFromGroup(this)")
        group.innerHTML = value
        row.appendChild(group)
    }
    select.remove()
    row.querySelector("#confirm_button").remove() // usuwa niepotrzebne przyciski
    generateAddToGroupButton(row) // dodaje nowy guzik do dodania nowego przedmiotu
}

function addToGroup(element){
    let row = element.parentElement
    element.remove()

    generateGroupSelect(row)
    generateConfirmButton(row)

}

function removeFromGroup(group_field){
    let select = group_field.parentElement.querySelector("#select")
    group_field.remove()
    if (select){
        updateSelection(select)
    }
    }

function generateAddToGroupButton(row){
    let add_group_button = document.createElement("button")
    add_group_button.setAttribute("id", "add_group_button")
    add_group_button.setAttribute("onclick", "addToGroup(this)")
    add_group_button.innerHTML = "+"
    row.appendChild(add_group_button)
}
function addStudent(){
    let student_name = document.getElementById("name-form").value
    let student_surname = document.getElementById("surname-form").value
    
    if(checkIfStudentInTable(student_name, student_surname)){
        return false
    }

    let row = document.createElement("tr")

    let del_button = document.createElement("button")
    // remove entire row when pressed
    del_button.setAttribute("onclick", "this.parentElement.remove()")
    del_button.innerHTML = "X"
    row.appendChild(del_button)
    
    
    let name = document.createElement("td")
    name.setAttribute("id", "name")
    name.innerHTML = student_name
    row.appendChild(name)
    
    let surname = document.createElement("td")
    surname.setAttribute("id", "surname")
    surname.innerHTML = student_surname
    row.appendChild(surname)

    generateAddToGroupButton(row)
    
    let table = document.getElementById("table")
    table.insertBefore(row, table.firstChild)

    return true
}

function populateTable(){
    textContent = textContent.trim()
    dane = textContent.split('\n')
    dane.forEach((element, index) => {
        dane[index] = element.split(' ')
    });
    // wczytanie rozszerzeń
    let roz = dane.shift()
    let group_list = document.getElementById("groups")
    group_list.innerHTML = ""
    roz.forEach(group => {
        generateGroupLi(group_list, group.replaceAll("_", " "))
    })
    // wczytanie wszystkich uczniów
    let table = document.getElementById("table")
    table.innerHTML = ""
    dane.forEach(student => {
        // console.log(student)
        let row = document.createElement("tr")
         
        let del_button = document.createElement("button")
        // remove entire row when pressed
        del_button.setAttribute("onclick", "this.parentElement.remove()")
        del_button.innerHTML = "X"
        row.appendChild(del_button)

        let name = document.createElement("td")
        name.setAttribute("id", "name")
        name.innerHTML = student.shift()
        row.appendChild(name)

        let surname = document.createElement("td")
        surname.setAttribute("id", "surname")
        surname.innerHTML = student.shift()
        row.appendChild(surname)

        while (student.length>0) {
            let group = document.createElement("button")
            let value = student.shift().replaceAll("_", " ")
            group.setAttribute("id", "group-field")
            group.setAttribute("onclick", "removeFromGroup(this)")
            group.innerHTML = value
            row.appendChild(group)
        }

        generateAddToGroupButton(row)
        table.appendChild(row)
    })
    // console.log(dane)
}

function generateFileFromTable(){
    // generuje plik z danych z tabelki do zapisania przez użytkownika
    let dane = ""

    let group_list = document.getElementById("groups")
    let groups = []

    for (const group of group_list.children) {
        groups.push(group.id.replaceAll(" ", "_"))
    }
    dane = dane.concat(groups.join(" "))

    let table = document.getElementById("table")

    for (row of table.children){
        dane = dane.concat("\n")
        for (td of row.children) {
            if (td.id == "name" || td.id == "surname" || td.id == "group-field"){
                dane = dane.concat(td.innerHTML.replaceAll(" ", "_"), " ")
            }
        }
    }
    dane = dane.replace(/ +$/gm, "")

    return dane 
    

    // console.log(dane)
}

function saveFileFromTable(){
    dane = generateFileFromTable()
    var myFile = new File([dane], "dane.vts", {type: "text/plain;charset=utf-8"});
    saveAs(myFile);
}

function processData(){
    var data = generateFileFromTable()
    fetch("/vts", {
        "body" : JSON.stringify({"data" : data}),
        "headers" : {"Content-Type" : "application/json"},
        "method": "POST"
    })
    .then((res) => {
        return res.json()
    })
    .then(
        data => {
            // console.log(data)
            let solution_wrapper = document.getElementById("solution_wrapper")
            solution_wrapper.style.display = "block";
            createFilters()
            showResponse(data)
        }
    )
    .catch((err) => console.log(err))
}

function showResponse(resp){
    
    let response_card = document.getElementById('answers');
    response_card.innerHTML = "";
    resp.forEach(row => {
        let new_row = document.createElement("tr")
        row.forEach(group =>{
            let button = document.createElement("button")
            button.innerHTML = group.replace("_", " ")
            new_row.appendChild(button)
        })
        response_card.appendChild(new_row)
    })
}

function createFilters(){
    let groups = Array.from(document.getElementById("groups").children)
    let filters = document.getElementById("filters")
    filters.innerHTML = ""
    groups.forEach(group => {
        let filter = document.createElement("button")
        filter.innerHTML = group.innerHTML
        filter.setAttribute("onclick", "updateFilters(this)")
        filters.appendChild(filter)
    })
}

function filterWith(filters){
    let answers = document.getElementById("answers").childNodes
    for (var row of answers) {
        var visible = true;
        var groups = [];
        for (const group of row.childNodes){
            groups.push(group.innerHTML)
        }
        filters.forEach(filter => {
            if (!groups.includes(filter))
            visible = false
        })
        
        row.style.display = (visible ? "block" : "none")
    }
    
}

function updateFilters(filter){
    filter.classList.toggle("inset")
    var active_filters = [];
    const filters = document.getElementById("filters").childNodes
    for (var filter of filters) {
        if (filter.classList.contains("inset")) {
            active_filters.push(filter.innerHTML)
        }
    }
    console.log(active_filters)
    filterWith(active_filters)
}


var editorInputFile = document.getElementById("file-form")
editorInputFile.onchange = (e) => {
    var file = editorInputFile.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (e) => {
        // e.target points to the reader
        textContent = e.target.result
        populateTable()
        // console.log(`The content of ${file.name} is \n${textContent}`)
        // populateTable()
    }
    reader.onerror = (e) => {
        const error = e.target.error
        console.error(`Error occured while reading ${file.name}`, error)
    }
    reader.readAsText(file)
    editorInputFile.value = null;
}