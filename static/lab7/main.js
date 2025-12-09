function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data){
        return data.json();
    })
    .then(function (films){
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            
            let tdTitleRus = document.createElement('td');
            
            
            let tdTitle = document.createElement('td');
            
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            
            tdTitleRus.innerHTML = films[i].title_ru;
            tdTitleRus.style.fontWeight = '500';
            
            
            let originalTitle = films[i].title;
            if (originalTitle && originalTitle !== films[i].title_ru) {
                
                let titleSpan = document.createElement('span');
                titleSpan.className = 'original-title';
                titleSpan.textContent = originalTitle;
                tdTitle.appendChild(titleSpan);
            } else {
                
                tdTitle.innerHTML = '<span style="color: #999; font-style: italic;">(нет)</span>';
            }
            
            tdYear.innerHTML = films[i].year;
            tdYear.style.fontWeight = '500';
            
            let buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'action-buttons';
            
            let editButton = document.createElement('button');
            editButton.className = 'edit-btn';
            editButton.innerText = 'Редактировать';
            editButton.onclick = function(){
                editFilm(i);
            }

            let delButton = document.createElement('button');
            delButton.className = 'delete-btn';
            delButton.innerText = 'Удалить';
            delButton.onclick = function(){
                deleteFilm(i, films[i].title_ru);
            }

            buttonsContainer.append(editButton);
            buttonsContainer.append(delButton);
            tdActions.appendChild(buttonsContainer);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
    .catch(error => {
        console.error('Ошибка загрузки фильмов:', error);
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #f44336; padding: 20px;">Ошибка загрузки данных</td></tr>';
    });
}
function deleteFilm(id, title) {
    if (! confirm(`Вы точно хотите удалить фильм? "${title}"?`))
        return

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function(){
        fillFilmList();
    });
}

function showModal(){
    document.getElementById('description-error').innerText = ''
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal(){
    document.querySelector('div.modal').style.display = 'none';
}

function cancel(){
    hideModal();
}
 
function addFilm(){
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';

    document.getElementById('description-error').innerText = '';
    showModal();
}


function sendFilm(){
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: document.getElementById('year').value,
        description: document.getElementById('description').value.trim()
    }

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    document.getElementById('description-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if (resp.ok){
            fillFilmList();
            hideModal();   
            return {};
        }
        return resp.json();
    })
    .then(function(errors){

        if (errors && Object.keys(errors).length > 0) {
            
            if (errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
            
            if (!errors.description && errors[Object.keys(errors)[0]]) {
                document.getElementById('description-error').innerText = errors[Object.keys(errors)[0]];
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        document.getElementById('description-error').innerText = 'Ошибка соединения с сервером';
    });
}
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data){
        return data.json();
    })
    .then(function (film){
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;

        document.getElementById('description-error').innerText = ''

        showModal()
    })
}