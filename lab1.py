from flask import Blueprint, url_for, request, redirect
lab1 = Blueprint('lab1', __name__)
import datetime


@lab1.route("/lab1")
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a> - Web сервер</li>
            <li><a href="/lab1/author">/lab1/author</a> - Информация об авторе</li>
            <li><a href="/lab1/image">/lab1/image</a> - Изображение</li>
            <li><a href="/lab1/counter">/lab1/counter</a> - Счетчик посещений</li>
            <li><a href="/lab1/reset_counter">/lab1/reset_counter</a> - Сброс счетчика</li>
            <li><a href="/lab1/info">/lab1/info</a> - Перенаправление</li>
            <li><a href="/lab1/created">/lab1/created</a> - Успешное создание</li>
            <li><a href="/400">/400</a> - Неверный запрос</li>
            <li><a href="/401">/401</a> - Не авторизован</li>
            <li><a href="/402">/402</a> - Необходима оплата</li>
            <li><a href="/403">/403</a> - Доступ запрещен</li>
            <li><a href="/405">/405</a> - Метод не разрешен</li>
            <li><a href="/418">/418</a> - Я чайник</li>
            <li><a href="/cause500">/cause500</a> - Вызвать ошибку 500</li>
        </ul>
        
        <a href="/">На главную</a>
    </body>
</html>
'''


@lab1.route("/400")
def bad_request():
    return "400 — Неверный запрос", 400


@lab1.route("/401")
def unauthorized():
    return "401 — Не авторизован", 401


@lab1.route("/402")
def payment_required():
    return "402 — Необходима оплата", 402


@lab1.route("/403")
def forbidden():
    return "403 — Доступ запрещён", 403


@lab1.route("/405")
def method_not_allowed():
    return "405 — Метод не разрешён", 405

@lab1.route("/418")
def teapot():
    return "418 — Я — чайник", 418


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href = "/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Кудеярова Яна Олеговна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
            <html>
                <body>
                    <p>Студент: """+ name +"""</p>
                    <p>Группа: """+ group +"""</p>
                    <p>Факультет: """+ faculty +"""</p>
                    <a href = "/web">web</a>
                </body>
            </html>"""


@lab1.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel = "stylesheet" href="''' + css_path +'''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
''',200, {
        'Content-Language': 'ru-RU',  
        'X-Custom-Header': 'MyCustomValue',  
        'X-Developer-Name': 'Yana-Kudeyarova' 
    }


count = 0


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    reset_url = url_for("reset_counter")
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) +'''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + ''' <br>
        Ваш IP-адрес: ''' + client_ip + ''' <br>
        <a href = "''' + reset_url + '''">Очистить счетчик</a>
    </body>
</html>
'''


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        Счётчик сброшен! <br>
        <a href="/lab1/counter">Вернуться к счётчику</a>
    </body>
</html>
'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201


@lab1.route("/cause500")
def cause500():
    return 1 / 0  



