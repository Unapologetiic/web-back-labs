from flask import Flask, url_for, request
import os
import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import path
from db.models import users
from flask_login import LoginManager
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретики для крысок')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'yana_ku_orm'
    db_user = 'yana_ku_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'

else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "yana_ku_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)

access_log = []

@app.route("/")
def start():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <hr>
        <ul>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href="/lab2">Вторая лабораторная</a></li>
            <li><a href="/lab3">Третья лабораторная</a></li>
            <li><a href="/lab4">Четвертая лабораторная</a></li>
            <li><a href="/lab5">Пятая лабораторная</a></li>
            <li><a href="/lab6">Шестая лабораторная</a></li>
            <li><a href="/lab7">Седьмая лабораторная</a></li>
            <li><a href="/lab8">Восьмая лабораторная</a></li>
            <li><a href="/lab9">Девятая лабораторная</a></li>
        </ul>
        <hr>
        <footer>
            Кудеярова Яна Олеговна, группа ФБИ-31, 2 курс, 2025 г.
        </footer>
    </body>
</html>
'''

@app.errorhandler(404)
def page_not_found(err):
    user_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    access_log.append({
        'ip': user_ip,
        'date': access_date,
        'url': requested_url
    })
    photo = url_for("static", filename="404.jpg")
    log_html = ""
    for entry in reversed(access_log[-5:]):
        log_html += '<tr><td>' + entry['ip'] + '</td><td>' + entry['date'] + '</td><td>' + entry['url'] + '</td></tr>'
    return '''
<!doctype html>
<html>
<head>
    <title>Страница не найдена (404)</title>
    <style>
        body { 
            background-color: #fdf6e3; 
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 { color: #dc143c; text-align: center; }
        p { color: #555; text-align: center; }
        .info { 
            background: #fff8e1; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 20px auto;
            max-width: 600px;
        }
        img { 
            max-width: 250px; 
            display: block;
            margin: 20px auto;
        }
        a { 
            color: #dc143c; 
            text-decoration: none;
            font-weight: bold;
        }
        a:hover { text-decoration: underline; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
        }
        th, td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #dc143c;
            color: white;
        }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Ой! Страница не найдена (404)</h1>
    
    <div class="info">
        <strong>IP-адрес:</strong> ''' + user_ip + '''<br>
        <strong>Дата:</strong> ''' + access_date + '''<br>
        <strong>Запрошено:</strong> ''' + requested_url + '''
    </div>
    
    <p>
        Вернитесь <a href="/">на главную страницу</a>
    </p>
    
    <img src="''' + photo + '''" alt="404 Error">
    
    <h3>Последние обращения:</h3>
    <table>
        <tr>
            <th>IP-адрес</th>
            <th>Дата</th>
            <th>URL</th>
        </tr>
        ''' + log_html + '''
    </table>
</body>
</html>
''', 404


@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка 500</title>
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>Что-то пошло не так. Попробуйте позже.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 500