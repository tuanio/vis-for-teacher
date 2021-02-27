let Ajax = function() {

    this.get = (url, callback) => {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = () => {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                callback(xhttp.responseText);
            }
        }
        xhttp.open('GET', url, true);
        xhttp.send();
    }

    this.post = (url, data, callback) => {
        // data is a json
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = () => {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                callback(xhttp.responseText);
            }
        }
        xhttp.open('POST', url, true);
        xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded;UTF-8');
        xhttp.send(data);
    }
}

let ajax = new Ajax();

// this function will run after the page is loaded

window.onload = () => {
    let width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

    var xhttp = new XMLHttpRequest()
    xhttp.open("GET", `/onload/${width}/${height}`, true);
    xhttp.send();
}

// hàm này dùng để kiểm tra phần tử có selector là tham số, trả về một promise
const checkElement = async selector => {
    while (!document.querySelector(selector)) {
        await new Promise(r => setTimeout(r, 500));
    }
    return document.querySelector(selector);
};
