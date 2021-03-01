// this function will run after the page is loaded

window.onload = () => {
    let width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

    var xhttp = new XMLHttpRequest()
    xhttp.open("GET", `/onload/${width}/${height}`, true);
    xhttp.send();
}

// hàm này dùng để kiểm tra phần tử có selector là tham số, trả về một promise
async function checkElement(selector) {
    while (!document.querySelector(selector)) {
        await new Promise(r => setTimeout(r, 200));
    }
    return document.querySelector(selector);
}