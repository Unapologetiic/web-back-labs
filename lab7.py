from flask import Blueprint, render_template, request, session, current_app, abort, jsonify
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    def db_connect():
        if current_app.config['DB_TYPE'] == 'postgres':
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='yana_kudeyariva_knowledge_base',
                user='yana_kudeyariva_knowledge_base',
                password='123'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        else:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, "database.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

        return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/index.html')

def validate_film_data(film_data):
    """Валидация данных фильма"""
    errors = {}
    
    # Проверка русского названия
    title_ru = film_data.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Введите название на русском языке'
    
    # Если оригинальное название не указано, используем русское
    title = film_data.get('title', '').strip()
    if title_ru and not title:
        film_data['title'] = title_ru
    
    # Проверка года
    current_year = datetime.datetime.now().year
    year = film_data.get('year')
    if year is not None:
        try:
            year_int = int(year)
            if year_int < 1895 or year_int > current_year:
                errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}'
            else:
                film_data['year'] = year_int
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    else:
        errors['year'] = 'Введите год выпуска'
    
    # Проверка описания
    description = film_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    return errors, film_data

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """Получить все фильмы из БД"""
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")
        
        films = cur.fetchall()
        
        # Конвертируем в список словарей
        films_list = []
        for film in films:
            if isinstance(film, dict):  # Для PostgreSQL с RealDictCursor
                films_list.append({
                    'id': film['id'],
                    'title': film['title'],
                    'title_ru': film['title_ru'],
                    'year': film['year'],
                    'description': film['description']
                })
            else:  # Для SQLite
                films_list.append({
                    'id': film[0],
                    'title': film[1],
                    'title_ru': film[2],
                    'year': film[3],
                    'description': film[4]
                })
        
        return jsonify(films_list)
    finally:
        db_close(conn, cur)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    """Получить фильм по ID из БД"""
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
        
        film = cur.fetchone()
        
        if not film:
            abort(404, description=f"Фильм с ID {id} не найден")
        
        if isinstance(film, dict):  # Для PostgreSQL
            film_dict = {
                'id': film['id'],
                'title': film['title'],
                'title_ru': film['title_ru'],
                'year': film['year'],
                'description': film['description']
            }
        else:  # Для SQLite
            film_dict = {
                'id': film[0],
                'title': film[1],
                'title_ru': film[2],
                'year': film[3],
                'description': film[4]
            }
        
        return jsonify(film_dict)
    finally:
        db_close(conn, cur)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    """Удалить фильм из БД"""
    conn, cur = db_connect()
    try:
        # Проверяем существование фильма
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        if not cur.fetchone():
            abort(404, description=f"Фильм с ID {id} не найден")
        
        # Удаляем фильм
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?", (id,))
        
        return '', 204
    finally:
        db_close(conn, cur)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Обновить фильм в БД"""
    conn, cur = db_connect()
    try:
        # Проверяем существование фильма
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        if not cur.fetchone():
            abort(404, description=f"Фильм с ID {id} не найден")
        
        # Получаем данные из запроса
        film = request.get_json()
        
        # Валидация данных
        errors, validated_film = validate_film_data(film)
        if errors:
            return jsonify(errors), 400
        
        # Обновляем данные в БД
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                UPDATE films 
                SET title = %s, title_ru = %s, year = %s, description = %s 
                WHERE id = %s
            """, (
                validated_film['title'],
                validated_film['title_ru'],
                validated_film['year'],
                validated_film['description'],
                id
            ))
        else:
            cur.execute("""
                UPDATE films 
                SET title = ?, title_ru = ?, year = ?, description = ? 
                WHERE id = ?
            """, (
                validated_film['title'],
                validated_film['title_ru'],
                validated_film['year'],
                validated_film['description'],
                id
            ))
        
        # Возвращаем обновленный фильм
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
        
        updated_film = cur.fetchone()
        
        if isinstance(updated_film, dict):
            return jsonify({
                'id': updated_film['id'],
                'title': updated_film['title'],
                'title_ru': updated_film['title_ru'],
                'year': updated_film['year'],
                'description': updated_film['description']
            })
        else:
            return jsonify({
                'id': updated_film[0],
                'title': updated_film[1],
                'title_ru': updated_film[2],
                'year': updated_film[3],
                'description': updated_film[4]
            })
    finally:
        db_close(conn, cur)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавить новый фильм в БД"""
    conn, cur = db_connect()
    try:
        # Получаем данные из запроса
        film = request.get_json()
        
        # Валидация данных
        errors, validated_film = validate_film_data(film)
        if errors:
            return jsonify(errors), 400
        
        # Вставляем данные в БД
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (
                validated_film['title'],
                validated_film['title_ru'],
                validated_film['year'],
                validated_film['description']
            ))
            new_id = cur.fetchone()['id']
        else:
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (?, ?, ?, ?)
            """, (
                validated_film['title'],
                validated_film['title_ru'],
                validated_film['year'],
                validated_film['description']
            ))
            new_id = cur.lastrowid
        
        return jsonify({"id": new_id})
    finally:
        db_close(conn, cur)