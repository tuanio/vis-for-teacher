// this function will run after the page is loaded

window.onload = () => {
    let width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

    var xhttp = new XMLHttpRequest()
    xhttp.open("GET", `/onload/${width}/${height}`, true);
    xhttp.send();
}