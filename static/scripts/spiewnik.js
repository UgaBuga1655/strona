function searchSong(title){
    let button = document.getElementById("submit")
    x = (title.length <3 ? '#' :  "/spiewnik/search/"+title)
    button.setAttribute("href", x)
}

function changeFontSize(value){
    let div = document.getElementById("songtext")
    let fontsize = div.style.fontSize.slice(0, -2);
    div.style.fontSize = parseInt(fontsize)+value+"px"
}