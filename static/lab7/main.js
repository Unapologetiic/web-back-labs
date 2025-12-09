async function fillFilmList() {
    const response = await fetch('/lab7/rest-api/films/');
    const films = await response.json();
    const tbody = document.getElementById('film-list');
    tbody.innerHTML = '';
    
    films.forEach(film => {
        const tr = document.createElement('tr');
        
        const titleCell = document.createElement('td');
        titleCell.textContent = film.title_ru;
        if (film.title !== film.title_ru) {
            const origTitle = document.createElement('span');
            origTitle.className = 'original-title';
            origTitle.textContent = film.title;
            titleCell.appendChild(document.createElement('br'));
            titleCell.appendChild(origTitle);
        }
        
        const origTitleCell = document.createElement('td');
        origTitleCell.textContent = film.title;
        
        const yearCell = document.createElement('td');
        yearCell.textContent = film.year;
        
        const actionCell = document.createElement('td');
        const actionButtons = document.createElement('div');
        actionButtons.className = 'action-buttons';
        
        const editButton = document.createElement('button');
        editButton.className = 'edit-btn';
        editButton.textContent = 'Редактировать';
        editButton.onclick = () => editFilm(film.id);
        
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-btn';
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = () => deleteFilm(film.id);
        
        actionButtons.appendChild(editButton);
        actionButtons.appendChild(deleteButton);
        actionCell.appendChild(actionButtons);
        
        tr.appendChild(titleCell);
        tr.appendChild(origTitleCell);
        tr.appendChild(yearCell);
        tr.appendChild(actionCell);
        tbody.appendChild(tr);
    });
}

async function deleteFilm(id) {
    if (!confirm('Вы уверены, что хотите удалить этот фильм?')) {
        return;
    }
    
    try {
        const response = await fetch(`/lab7/rest-api/films/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            await fillFilmList();
        } else {
            alert('Ошибка при удалении фильма');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка сети');
    }
}

async function editFilm(id) {
    try {
        const response = await fetch(`/lab7/rest-api/films/${id}`);
        const film = await response.json();
        
        document.getElementById('id').value = film.id;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('title').value = film.title;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        
        showModal();
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка при загрузке данных фильма');
    }
}

async function sendFilm() {
    const id = document.getElementById('id').value;
    const titleRu = document.getElementById('title-ru').value.trim();
    const title = document.getElementById('title').value.trim();
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value.trim();
    
    document.getElementById('description-error').textContent = '';
    
    const filmData = {
        title_ru: titleRu,
        title: title || titleRu,
        year: year,
        description: description
    };
    
    try {
        let response;
        if (id) {
            response = await fetch(`/lab7/rest-api/films/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(filmData)
            });
        } else {
            response = await fetch('/lab7/rest-api/films/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(filmData)
            });
        }
        
        const result = await response.json();
        
        if (!response.ok) {
            if (result.description) {
                document.getElementById('description-error').textContent = result.description;
            }
            if (result.year) {
                alert(`Ошибка в поле "Год": ${result.year}`);
            }
            if (result.title_ru) {
                alert(`Ошибка в поле "Название": ${result.title_ru}`);
            }
            return;
        }
        
        hideModal();
        await fillFilmList();
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка сети');
    }
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').textContent = '';
    
    showModal();
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.getElementById('modal-overlay').style.display = 'block';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
    document.getElementById('modal-overlay').style.display = 'none';
}

function cancel() {
    hideModal();
}