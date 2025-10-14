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
    return render_template('lab3/ticket_form.html')

@lab3.route('/lab3/ticket_result')
def ticket_result():
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

    return render_template('lab3/ticket_result.html', 
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, price=price)