from flask import Flask, url_for, request
import datetime 
from lab1 import lab1
from lab2 import lab2

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)

access_log = []

@app.route("/")
def index():
    return "Главная страница"

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
        <h1>Внутренняя ошибка сервера (500)</h1>
        <p>Что-то пошло не так. Попробуйте позже.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 500