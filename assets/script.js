// this function will run after the page is loaded
window.onload = () => {
    var xhttp = new XMLHttpRequest()
    xhttp.open("GET", '/onload', true);
    xhttp.send();
}