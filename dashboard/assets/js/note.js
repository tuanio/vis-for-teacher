checkElement('#show-note-btn').then((selector) => {
    selector.addEventListener('click', () => {
        toggleNoteListAndEdit(false);
    });
});

function createDivNoteComponent(data) {
    let divNoteComponent = document.createElement('div');
    divNoteComponent.setAttribute('class', 'note-component');
    divNoteComponent.setAttribute('data-id', `${data['id']}`);

    let divNoteDiv = document.createElement('div');
    divNoteDiv.setAttribute('class', 'note-div');

    let aNoteA = document.createElement('a');
    aNoteA.setAttribute('href', `javascript:viewNote(${data['id']})`);
    aNoteA.setAttribute('class', 'note-a');

    let h5NoteBigLabel = document.createElement('h5');
    h5NoteBigLabel.setAttribute('class', 'note-big-label');
    h5NoteBigLabel.textContent = `${data['title_shorten']}`;

    let pNoteSmLabel = document.createElement('p');
    pNoteSmLabel.setAttribute('class', 'note-sm-label');
    pNoteSmLabel.textContent = `Cập nhật mới nhất: ${data['date_update_format']}`;

    aNoteA.appendChild(h5NoteBigLabel);
    aNoteA.appendChild(pNoteSmLabel);
    divNoteDiv.appendChild(aNoteA);
    divNoteComponent.appendChild(divNoteDiv);
    return divNoteComponent;
}

function toggleNoteEdit(flag = false) {
    /*
        - xét sự kiện bật tắt cho div note edit, true thì bật, false thì tắt
    */
    let editNote = document.querySelector('#edit-note');
    editNote.style.display = flag ? 'block' : 'none';
}

function toggleNoteListAndEdit(editFlag = false) {
    // set sự kiện cho nút nhấn
    /*
        - khi mà nhấn nút sẽ thay đổi trạng thái của data-flag, 1 nghĩa là có show, 0 nghĩa là không show
        - editFlag là flag bật tắt của div edit note
        - flag là flag bật tắt của div list note
    */
    checkElement('.note-container').then((selec) => {
        let flag = parseInt(selec.getAttribute('data-flag'));
        selec.style.display = flag ? 'none' : 'block';
        selec.setAttribute('data-flag', 1 ^ flag);
        toggleNoteEdit(flag & editFlag);
        // đổi class cho thẻ a, nghĩa là đổi giao diện của thẻ dựa trên bootstrap
        document.querySelector('#show-note-btn-a').className = 'btn btn-' + (!flag ? 'success' : 'outline-success');

    });
}

checkElement('#add-note-btn a').then((selector) => {
    selector.addEventListener('click', () => {
        // react-select-5--value-item is a dropdown selector
        let dropdownNote = document.querySelector('#react-select-5--value-item');
        let showNote = document.querySelector('#show-note');
        (async () => {
            let response = await fetch(`/add-note/${dropdownNote.textContent}`);
            let json = await response.json();
            showNote.appendChild(createDivNoteComponent(json));
        })();
    });
});

function viewNote(id) {
    (async () => {
        let response = await fetch(`/view-note/${id}`);
        let data = await response.json();
        let noteTemplate = `
            <div>
                <p class="note-sm-label">Cập nhật mới nhất: ${data['date_update_format']}</p>
            </div>
            <div id="note-edit-title">
                <input type="text" id="note-edit-title-input" placeholder="Tiêu đề" class='form-control' value="${data['title']}">
            </div>
            <div id="note-edit-content">
                <textarea name="txt" id="note-edit-txtarea" placeholder="Nội dung ghi chú" class="form-control">${data['content']}</textarea>
            </div>
            <div id="note-edit-tools">
                <div id="note-edit-save">
                    <a href="javascript:saveNote(${data['id']});" class="btn btn-outline-success">Lưu thay đổi</a>
                </div>
                <div id="note-edit-remove">
                    <a href="javascript:deleteNote(${data['id']});" class="btn btn-outline-dark">
                        <i class="fas fa-trash"></i>
                    </a>
                </div>
            </div>
        `;
        document.querySelector('#edit-note').innerHTML = noteTemplate;
        toggleNoteListAndEdit(true);
    })();
}

function saveNote(id) {
    let title = document.querySelector('#note-edit-title-input').value;
    let content = document.querySelector('#note-edit-txtarea').value;
    // var has larger scope than let
    var data = {id, title, content};

    (async () => {
        let response = await fetch('/save-note', {
            method: 'POST',
            headers: {'Content-type': 'application/x-www-form-urlencoded;UTF-8'},
            body: JSON.stringify(data)
        });
        let json = await response.json();
        toggleNoteListAndEdit(false);
        // gán trở lại cái title_shorten để hiện thị trong danh sách note
        document.querySelector(`.note-component[data-id="${id}"] > div > a > h5`).innerHTML = json['title_shorten'];
        document.querySelector(`.note-component[data-id="${id}"] > div > a > p`).innerHTML = 'Cập nhật mới nhất: ' + json['date_update_format'];
    })().catch(console.log);
}

function deleteNote(id) {
    // form xác nhận hiện tại cứ sử dụng cái này
    let result = confirm('Bạn có chắc muốn xóa ghi chú không');
    if (result === true) {
        fetch(`/delete-note/${id}`);
        toggleNoteListAndEdit(false);
        // xóa theo data-id, xóa note khi đã nhấn
        let el = document.querySelector(`.note-component[data-id="${id}"]`);
        el.remove();
    }
}

// hàm cho callback clientside
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        callback_note: (data) => {
            data = eval(data);
            if (!data) return '';
            let showNote = document.querySelector('#show-note');
            showNote.innerHTML = '';
            for (let i = 0; i < data.length; i++) {
                showNote.appendChild(createDivNoteComponent(data[i]));
            }
            return "html.Div('okbro')";
        }
    }
});