from flask import Blueprint, render_template, request, make_response, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'yana_kudeyariva_knowledge_base',
            user = 'yana_kudeyariva_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn,cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error='Заполните поля')
    
    conn, cur = db_connect()

    db_type = current_app.config['DB_TYPE']

    if db_type == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'],password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    real_name = request.form.get('real_name')
    login = request.form.get('login')
    password = request.form.get('password')

    if not(real_name or login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    db_type = current_app.config['DB_TYPE']
    
    if db_type == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)
    if db_type == 'postgres':
        cur.execute("INSERT INTO users (real_name, login, password) VALUES (%s, %s, %s);", 
                   (real_name, login, password_hash))
    else:
        cur.execute("INSERT INTO users (real_name, login, password) VALUES (?, ?, ?);", 
                   (real_name, login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)
    
@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'

    if not title or not article_text:
        return render_template('lab5/create_article.html', 
                             error='Заполните название и текст статьи',
                             title=title, article_text=article_text)

    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    
    if db_type == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()["id"]

    if db_type == 'postgres':
        cur.execute("INSERT INTO articles (login_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);", 
                (login_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("INSERT INTO articles (login_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);", 
                (login_id, title, article_text, is_favorite, is_public))
    
    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    db_type = current_app.config['DB_TYPE']
    
    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()["id"]

    # Сортируем: сначала избранные, потом обычные
    if db_type == 'postgres':
        cur.execute("SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC, id DESC;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC, id DESC;", (login_id,))
    
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    
    # Получаем пользователя
    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user['id']
    
    if request.method == 'GET':
        # Получаем статью для редактирования
        if db_type == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND login_id=%s;", (article_id, user_id))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?;", (article_id, user_id))
        
        article = cur.fetchone()
        db_close(conn, cur)
        
        if not article:
            return redirect('/lab5/list')
        
        return render_template('lab5/edit_article.html', article=article)
    
    else:
        # POST - сохраняем изменения
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        
        if not title or not article_text:
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', 
                                 article={'id': article_id, 'title': title, 'article_text': article_text},
                                 error='Заполните название и текст статьи')
        
        # Обновляем статью
        if db_type == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s AND login_id=%s;", 
                       (title, article_text, article_id, user_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=? AND login_id=?;", 
                       (title, article_text, article_id, user_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
    
@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    
    # Получаем пользователя
    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if user:
        user_id = user['id']
        # Удаляем статью
        if db_type == 'postgres':
            cur.execute("DELETE FROM articles WHERE id=%s AND login_id=%s;", (article_id, user_id))
        else:
            cur.execute("DELETE FROM articles WHERE id=? AND login_id=?;", (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    
    if db_type == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY real_name;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY real_name;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    
    if request.method == 'GET':
        # Получаем текущие данные пользователя
        if db_type == 'postgres':
            cur.execute("SELECT real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        
        return render_template('lab5/profile.html', user=user)
    
    else:
        # Обрабатываем изменение данных
        real_name = request.form.get('real_name')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Получаем текущего пользователя
        if db_type == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        
        errors = []
        
        # Проверяем текущий пароль, если меняется пароль
        if new_password:
            if not current_password:
                errors.append('Введите текущий пароль для смены пароля')
            elif not check_password_hash(user['password'], current_password):
                errors.append('Текущий пароль неверен')
            elif new_password != confirm_password:
                errors.append('Новый пароль и подтверждение не совпадают')
            elif len(new_password) < 3:
                errors.append('Пароль должен быть не менее 3 символов')
        
        if errors:
            db_close(conn, cur)
            return render_template('lab5/profile.html', user=user, errors=errors)
        
        # Обновляем данные
        if new_password:
            password_hash = generate_password_hash(new_password)
            if db_type == 'postgres':
                cur.execute("UPDATE users SET real_name=%s, password=%s WHERE login=%s;", 
                           (real_name, password_hash, login))
            else:
                cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;", 
                           (real_name, password_hash, login))
        else:
            if db_type == 'postgres':
                cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (real_name, login))
            else:
                cur.execute("UPDATE users SET real_name=? WHERE login=?;", (real_name, login))
        
        db_close(conn, cur)
        return render_template('lab5/profile_success.html')
    
@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    
    # Получаем публичные статьи с именами авторов
    if db_type == 'postgres':
        cur.execute("""
            SELECT a.*, u.real_name, u.login 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = true 
            ORDER BY a.id DESC;
        """)
    else:
        cur.execute("""
            SELECT a.*, u.real_name, u.login 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = 1 
            ORDER BY a.id DESC;
        """)
    
    articles = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/public_articles.html', articles=articles)