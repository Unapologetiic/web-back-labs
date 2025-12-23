from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash
from db import db
from db.models import users

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8/')
def lab():
    # Получаем логин из сессии или используем 'anonymous'
    username = session.get('login', 'anonymous')
    login = session.get('login')
    return render_template('lab8/lab8.html', username=username, login=login)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Проверка на пустые значения 
    if not login_form or not password_form:
        return render_template('lab8/register.html', 
                             error='Логин и пароль не должны быть пустыми')
    
    # Поиск пользователя в БД 
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                             error='Такой пользователь уже существует')
    
    # Хеширование пароля и создание пользователя 
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    # Добавление в БД 
    db.session.add(new_user)
    db.session.commit()
    
    # Автоматический вход после регистрации
    session['login'] = login_form
    
    # Перенаправление на главную
    return redirect('/lab8/')