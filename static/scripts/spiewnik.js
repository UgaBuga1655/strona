function searchSong(title){
    let button = document.getElementById("submit")
    button.setAttribute("href", "/spiewnik/search/"+title)
}

function changeFontSize(value){
    let div = document.getElementById("songtext")
    let fontsize = div.style.fontSize.slice(0, -2);
    div.style.fontSize = parseInt(fontsize)+value+"px"
}