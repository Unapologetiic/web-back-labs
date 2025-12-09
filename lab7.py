from flask import Blueprint, render_template, request, session, current_app, abort, jsonify
import datetime  # Добавим для получения текущего года

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/index.html')

films = [
    {
        "title": "The Gentlemen",
        "title_ru": "Джентльмены",
        "year": 2019,
        "description": "Гангстеры всех мастей делят наркоферму. Закрученная экшен-комедия Гая Ричи с Мэттью Макконахи и Хью Грантом"
    },
    {
        "title": "Shutter Island",
        "title_ru": "Остров проклятых",
        "year": 2009,
        "description": "Двое приставов расследуют побег пациентки из мрачной психбольницы. Параноидальный триллер с Леонардо ДиКаприо"
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Бессонница, драки и мыло. Контркультурный шедевр Дэвида Финчера, который можно пересматривать бесконечно"
    },
    {
        "title": "1+1",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Аристократ на коляске нанимает в сиделки бывшего заключенного. Искрометная французская комедия с Омаром Си"
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб не верил в чудеса. Пока не столкнулся с одним из них"
    },
]

def validate_film_data(film_data):
    """Валидация данных фильма"""
    errors = {}
    

    if not film_data.get('title_ru', '').strip():
        errors['title_ru'] = 'Введите название на русском языке'
    
    if film_data.get('title_ru', '').strip() and not film_data.get('title', '').strip():
        film_data['title'] = film_data['title_ru']
    

    current_year = datetime.datetime.now().year
    year = film_data.get('year')
    if year is not None:
        try:
            year_int = int(year)
            if year_int < 1895 or year_int > current_year:
                errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    else:
        errors['year'] = 'Введите год выпуска'
    
    
    description = film_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    return errors, film_data

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с индексом {id} не найден")
    return jsonify(films[id]) 

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с индексом {id} не найден")
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с индексом {id} не найден")
    
    film = request.get_json()
    
    # Валидация данных
    errors, validated_film = validate_film_data(film)
    if errors:
        return jsonify(errors), 400
    
    films[id] = validated_film
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Валидация данных
    errors, validated_film = validate_film_data(film)
    if errors:
        return jsonify(errors), 400
    
    films.append(validated_film)
    new_id = len(films) - 1
    return jsonify({"id": new_id})