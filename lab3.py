from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    if name:
        display_name = name
        display_color = name_color  
    else:
        display_name = "Аноним"
        display_color = "#000000"  
    
    return render_template('lab3/lab3.html', name=display_name, name_color=display_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 85

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 30
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')   
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    
    if color or bg_color or font_size or font_family:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        return resp
    
    color_from_cookie = request.cookies.get('color', '#000000')
    bg_color_from_cookie = request.cookies.get('bg_color', '#ffffff')
    font_size_from_cookie = request.cookies.get('font_size', '16px')
    font_family_from_cookie = request.cookies.get('font_family', 'Arial')
    
    return render_template('lab3/settings.html', 
                         color=color_from_cookie,
                         bg_color=bg_color_from_cookie,
                         font_size=font_size_from_cookie,
                         font_family=font_family_from_cookie)

@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket.html')

@lab3.route('/lab3/ticket2')
def ticket2():
    # Получаем данные из формы
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen') == 'on'
    luggage = request.args.get('luggage') == 'on'
    age = int(request.args.get('age'))
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance') == 'on'

    if age < 1 or age > 120:
        return "Возраст должен быть от 1 до 120 лет", 400

    
    if age < 18:
        price = 700  
    else:
        price = 1000  

    if shelf in ['lower', 'lower-side']:
        price += 100  
    
    if linen:
        price += 75  
    
    if luggage:
        price += 250  
    
    if insurance:
        price += 150  

    return render_template('lab3/ticket2.html', 
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, price=price)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp


products_list = [
    {'name': 'iPhone 15 Pro', 'price': 99990, 'brand': 'Apple', 'color': 'Титановый', 'storage': 128},
    {'name': 'Samsung Galaxy S24', 'price': 79990, 'brand': 'Samsung', 'color': 'Черный', 'storage': 256},
    {'name': 'Xiaomi 14', 'price': 59990, 'brand': 'Xiaomi', 'color': 'Белый', 'storage': 256},
    {'name': 'Google Pixel 8', 'price': 69990, 'brand': 'Google', 'color': 'Серый', 'storage': 128},
    {'name': 'OnePlus 12', 'price': 54990, 'brand': 'OnePlus', 'color': 'Зеленый', 'storage': 256},
    {'name': 'iPhone 14', 'price': 74990, 'brand': 'Apple', 'color': 'Синий', 'storage': 128},
    {'name': 'Samsung Galaxy A54', 'price': 29990, 'brand': 'Samsung', 'color': 'Фиолетовый', 'storage': 128},
    {'name': 'Xiaomi Redmi Note 13', 'price': 19990, 'brand': 'Xiaomi', 'color': 'Черный', 'storage': 64},
    {'name': 'Realme 11 Pro+', 'price': 24990, 'brand': 'Realme', 'color': 'Золотой', 'storage': 256},
    {'name': 'Nothing Phone 2', 'price': 44990, 'brand': 'Nothing', 'color': 'Белый', 'storage': 128},
    {'name': 'iPhone 13', 'price': 59990, 'brand': 'Apple', 'color': 'Розовый', 'storage': 128},
    {'name': 'Samsung Galaxy Z Flip5', 'price': 89990, 'brand': 'Samsung', 'color': 'Сиреневый', 'storage': 256},
    {'name': 'Xiaomi Poco X6 Pro', 'price': 27990, 'brand': 'Xiaomi', 'color': 'Желтый', 'storage': 256},
    {'name': 'Honor Magic6 Lite', 'price': 22990, 'brand': 'Honor', 'color': 'Синий', 'storage': 128},
    {'name': 'Vivo V29', 'price': 34990, 'brand': 'Vivo', 'color': 'Красный', 'storage': 256},
    {'name': 'Oppo Reno 10', 'price': 31990, 'brand': 'Oppo', 'color': 'Зеленый', 'storage': 128},
    {'name': 'iPhone 15', 'price': 84990, 'brand': 'Apple', 'color': 'Черный', 'storage': 128},
    {'name': 'Samsung Galaxy S23 FE', 'price': 49990, 'brand': 'Samsung', 'color': 'Кремовый', 'storage': 128},
    {'name': 'Xiaomi 13T', 'price': 44990, 'brand': 'Xiaomi', 'color': 'Черный', 'storage': 256},
    {'name': 'Google Pixel 7a', 'price': 39990, 'brand': 'Google', 'color': 'Белый', 'storage': 128}
]

@lab3.route('/lab3/products')
def products():

    min_price_all = min(product['price'] for product in products_list)
    max_price_all = max(product['price'] for product in products_list)
    

    min_price = request.args.get('min_price') or request.cookies.get('products_min_price')
    max_price = request.args.get('max_price') or request.cookies.get('products_max_price')
    
    filtered_products = products_list.copy()
    
    if min_price:
        min_price = int(min_price)
        filtered_products = [p for p in filtered_products if p['price'] >= min_price]
    
    if max_price:
        max_price = int(max_price)
        filtered_products = [p for p in filtered_products if p['price'] <= max_price]
    
    if min_price and max_price and min_price > max_price:
        min_price, max_price = max_price, min_price
        filtered_products = [p for p in products_list if min_price <= p['price'] <= max_price]
    
    resp = make_response(render_template('lab3/products.html', 
                                       products=filtered_products,
                                       min_price=min_price,
                                       max_price=max_price,
                                       min_price_all=min_price_all,
                                       max_price_all=max_price_all))
    
    if min_price:
        resp.set_cookie('products_min_price', str(min_price))
    if max_price:
        resp.set_cookie('products_max_price', str(max_price))
    
    return resp

@lab3.route('/lab3/products_reset')
def products_reset():
    resp = make_response(redirect('/lab3/products'))
    resp.delete_cookie('products_min_price')
    resp.delete_cookie('products_max_price')
    return resp