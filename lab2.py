from flask import Blueprint, request, redirect, render_template, abort

lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшом'

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330}
]

@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', flowers=flower_list)

@lab2.route('/lab2/add_flower/')
def add_flower():
    name = request.args.get('name')
    if not name:
        return "вы не задали имя цветка", 400
    flower_list.lab2end({'name': name, 'price': 300})
    return redirect('/lab2/all_flowers')

@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/all_flowers')

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')

@lab2.route('/lab2/example')
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

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')
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

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
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

@lab2.route('/lab2/books')
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

@lab2.route('/lab2/cats')
def cats_list():
    return render_template('cats.html', cats=cats)