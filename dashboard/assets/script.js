let Ajax = function() {
    // this.get = (url) => {
    //     return new Promise((resolve, reject) => {
    //         let xhttp = new XMLHttpRequest();
    //         xhttp.onreadystatechange = () => {
    //             if (xhttp.readyState = 4 && xhttp.status == 200) {
    //                 resolve(xhttp.responseText);
    //             }
    //         }
    //         xhttp.open('GET', url, true);
    //         xhttp.send();
    //     });
    // }

    this.get = (url, callback) => {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = () => {
            if (xhttp.readyState = 4 && xhttp.status == 200) {
                callback(xhttp.responseText);
            }
        }
        xhttp.open('GET', url, true);
        xhttp.send();
    }

    this.post = (url, data) => {
        return new Promise((resolve, reject) => {
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = () => {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                    resolve(xhttp.responseText);
                }
            }
            xhttp.open('POST', url, true);
            xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded;UTF-8');
            xhttp.send(data);
        });
    }
}

let ajax = new Ajax();

// this function will run after the page is loaded

window.onload = () => {
    let width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

    fetch(`/onload/${width}/${height}`);
    // var xhttp = new XMLHttpRequest()
    // xhttp.open("GET", `/onload/${width}/${height}`, true);
    // xhttp.send();
}

const checkElement = async selector => {
    while (!document.querySelector(selector)) {
        await new Promise(r => setTimeout(r, 500));
    }
    return document.querySelector(selector);
};

checkElement('#show-note-btn').then((selector) => {
    selector.addEventListener('click', () => {

        // set sự kiện cho nút nhấn
        /*
            - khi mà nhấn nút sẽ thay đổi trạng thái của data-flag, 1 nghĩa là có show, 0 nghĩa là không show
        */

        checkElement('.note-container').then((selec) => {
            let flag = parseInt(selec.getAttribute('data-flag'));
            selec.style.display = flag ? 'none' : 'block';
            selec.setAttribute('data-flag', 1 ^ flag);

            // đổi class cho thẻ a, nghĩa là đổi giao diện của thẻ dựa trên bootstrap
            document.querySelector('#show-note-btn-a').className = 'btn btn-' + (!flag ? 'success' : 'outline-success');
        });
    });
});

function check(ok) {
    console.log(ok);
}

checkElement('#add-note-btn a').then((selector) => {
    selector.addEventListener('click', () => {
        
        // react-select-5--value-item is a dropdown selector
        let dropdownNote = document.querySelector('#react-select-5--value-item');
        
        let showNote = document.querySelector('#show-note');

        ajax.get(`/add-note/${dropdownNote.textContent}`, (data) => {
            data = JSON.stringify(data);
            let currentDate = new Date();
            let templateNote = `
                <div class="note-component">
                    <div class="note-div">
                        <a href="javascript:void(0);" data-id="${data['id']}" class="note-a">
                            <h5 class="note-big-label">
                                Tiêu đề ghi chú...
                            </h5>
                            <p class="note-sm-label">Cập nhật mới nhất: ${currentDate.getHours().toString().padStart(2, '0')}:${currentDate.getMinutes().toString().padStart(2, '0')} ${currentDate.getDay().toString().padStart(2, '0')}/${currentDate.getMonth().toString().padStart(2, '0')}/${currentDate.getFullYear()}
                            </p>
                        </a>
                    </div>
                </div>
            `;
            showNote.innerHTML += templateNote;
        });
    });
});