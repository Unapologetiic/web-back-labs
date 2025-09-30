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
            <li><a href="/lab2">Вторая лабораторная</a></li>
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

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330}
]

@app.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', flowers=flower_list)

@app.route('/lab2/add_flower/')
def add_flower():
    name = request.args.get('name')
    if not name:
        return "вы не задали имя цветка", 400
    flower_list.append({'name': name, 'price': 300})
    return redirect('/lab2/all_flowers')

@app.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/all_flowers')

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')

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

cats = [
    {
        'name': 'Британская короткошёрстная',
        'image': 'british.jpg',
        'description': 'Крепкая кошка с плюшевой шерстью и круглыми глазами. Очень спокойная и независимая.'
    },
    {
        'name': 'Мейн-кун',
        'image': 'maine_coon.jpg', 
        'description': 'Крупная порода с длинной шерстью и кисточками на ушах. Дружелюбные и игривые гиганты.'
    },
    {
        'name': 'Сиамская',
        'image': 'siamese.jpg',
        'description': 'Элегантная кошка с ярко-голубыми глазами и контрастным окрасом. Очень общительная и разговорчивая.'
    },
    {
        'name': 'Сфинкс',
        'image': 'sphynx.jpg',
        'description': 'Бесшёрстная порода с морщинистой кожей. Теплолюбивые и очень ласковые кошки.'
    },
    {
        'name': 'Персидская',
        'image': 'persian.jpg',
        'description': 'Длинношёрстная кошка с приплюснутой мордочкой. Спокойная и аристократичная порода.'
    },
    {
        'name': 'Шотландская вислоухая',
        'image': 'scottish_fold.jpg',
        'description': 'Кошки с загнутыми вперёд ушами и круглыми глазами. Дружелюбные и адаптивные.'
    },
    {
        'name': 'Бенгальская',
        'image': 'bengal.jpg',
        'description': 'Порода с леопардовым окрасом и дикой внешностью. Очень активные и умные кошки.'
    },
    {
        'name': 'Русская голубая',
        'image': 'russian_blue.jpg',
        'description': 'Кошка с серебристо-голубой шерстью и зелёными глазами. Скромная и преданная.'
    },
    {
        'name': 'Норвежская лесная',
        'image': 'norwegian_forest.jpg',
        'description': 'Крупная кошка с густой водонепроницаемой шерстью. Отличный охотник и лазальщик.'
    },
    {
        'name': 'Ориентальная',
        'image': 'oriental.jpg',
        'description': 'Стройная кошка с большими ушами и грациозным телом. Очень энергичная и общительная.'
    },
    {
        'name': 'Рэгдолл',
        'image': 'ragdoll.jpg',
        'description': 'Крупная кошка с мягкой шерстью и голубыми глазами. Расслабляется на руках как тряпичная кукла.'
    },
    {
        'name': 'Абиссинская',
        'image': 'abyssinian.jpg',
        'description': 'Короткошёрстная кошка с тикированным окрасом. Любопытная и активная порода.'
    },
    {
        'name': 'Бирманская',
        'image': 'birman.jpg',
        'description': 'Полудлинношёрстная кошка с белыми "носочками". Спокойная и преданная порода.'
    },
    {
        'name': 'Турецкий ван',
        'image': 'turkish_van.jpg',
        'description': 'Кошка с уникальной любовью к воде и красно-белым окрасом. Активная и умная.'
    },
    {
        'name': 'Египетский мау',
        'image': 'egyptian_mau.jpg',
        'description': 'Пятнистая кошка с зелёными глазами. Одна из древнейших пород, очень быстрая.'
    },
    {
        'name': 'Тонкинская',
        'image': 'tonkinese.jpg',
        'description': 'Порода среднего размера с аквамариновыми глазами. Общительная и игривая.'
    },
    {
        'name': 'Корниш-рекс',
        'image': 'cornish_rex.jpg',
        'description': 'Кошка с волнистой шерстью и стройным телом. Очень активная и любознательная.'
    },
    {
        'name': 'Девон-рекс',
        'image': 'devon_rex.jpg',
        'description': 'Кошка с крупными ушами и волнистой шерстью. Игривая и привязчивая порода.'
    },
    {
        'name': 'Сибирская',
        'image': 'siberian.jpg',
        'description': 'Крупная кошка с густой трёхслойной шерстью. Гипоаллергенная и преданная порода.'
    },
    {
        'name': 'Манчкин',
        'image': 'munchkin.jpg',
        'description': 'Кошка с короткими лапами при нормальном размере тела. Игривая и общительная.'
    },
    {
        'name': 'Бомбейская',
        'image': 'bombay.jpg',
        'description': 'Чёрная кошка с блестящей шерстью и медными глазами. Напоминает миниатюрную пантеру.'
    },
    {
        'name': 'Японский бобтейл',
        'image': 'japanese_bobtail.jpg',
        'description': 'Кошка с коротким хвостом-помпоном. Активная и разговорчивая порода.'
    }
]

@app.route('/lab2/cats')
def cats_list():
    return render_template('cats.html', cats=cats)