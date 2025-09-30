from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask (__name__)

@app.route("/")
@app.route("/index")
def index():
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
        </ul>
        <hr>
        <footer>
            Кудеярова Яна Олеговна, группа ФБИ-31, 2 курс, 2025 г.
        </footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
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

@app.route("/400")
def bad_request():
    return "400 — Неверный запрос", 400

@app.route("/401")
def unauthorized():
    return "401 — Не авторизован", 401

@app.route("/402")
def payment_required():
    return "402 — Необходима оплата", 402

@app.route("/403")
def forbidden():
    return "403 — Доступ запрещён", 403

@app.route("/405")
def method_not_allowed():
    return "405 — Метод не разрешён", 405

@app.route("/418")
def teapot():
    return "418 — Я — чайник", 418

access_log = []

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

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route("/lab1/image")
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

@app.route('/lab1/counter')
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

@app.route('/lab1/reset_counter')
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
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

@app.route("/cause500")
def cause500():
    return 1 / 0  

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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшом'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len (flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <title>Цветок #{flower_id}</title>
    </head>
    <body>
        <h1>Информация о цветке</h1>
        <p><strong>ID цветка:</strong> {flower_id}</p>
        <p><strong>Название:</strong> {flower_list[flower_id]}</p>
        <p><strong>Всего цветов в базе:</strong> {len(flower_list)}</p>
        <hr>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {", ".join(flower_list)}</p>
    <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html> 
''' 

@app.route('/lab2/add_flower/')
def add_flower_empty():
    return "вы не задали имя цветка", 400

@app.route('/lab2/all_flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <head>
        <title>Все цветы</title>
    </head>
    <body>
        <h1>Список всех цветов</h1>
        <p><strong>Всего цветов:</strong> {len(flower_list)}</p>
        <ul>
            {"".join([f"<li>{i}. {flower}</li>" for i, flower in enumerate(flower_list)])}
        </ul>
        <hr>
        <a href="/lab2/clear_flowers">Очистить список цветов</a>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <p>Все цветы были удалены из списка.</p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Яна Кудеярова'
    group = 'ФБИ-31'
    course = '3 курс'
    lab_num = 2
    fruits = [
        {'name': 'яблоки', 'price':100},
        {'name': 'груши', 'price':120},
        {'name': 'апельсины', 'price':80},
        {'name': 'мандарины', 'price':90},
        {'name': 'манго', 'price':321}
    ]
    return render_template('example.html', name=name, group=group, course=course, 
                           lab_num=lab_num, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
<!doctype html>
<html>
    <head>
        <title>Калькулятор</title>
    </head>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {a + b}</p>
        <p>{a} - {b} = {a - b}</p>
        <p>{a} * {b} = {a * b}</p>
        <p>{a} / {b} = {a / b}</p>
        <p>{a}<sup>{b}</sup> = {a ** b}</p>
    </body>
</html>
'''

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказы', 'pages': 320},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 640},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 128},
    {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]

@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)