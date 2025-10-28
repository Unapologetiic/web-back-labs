from flask import Blueprint, render_template, request, make_response, redirect, session

lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error= 'Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error= 'Ошибка: деление на ноль невозможно!')
    
    result = x1/x2
    return render_template('lab4/div.html' , x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 0
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 0
    else:
        x2 = int(x2)
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods = ['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods = ['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Ошибка: ноль в нулевой степени не определен!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count=0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count = tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < 10:
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Иванов', 'gender': 'male'},
    {'login': 'anna', 'password': '321', 'name': 'Анна Сидорова', 'gender': 'female'},
    {'login': 'lola', 'password': '666', 'name': 'Лола Ким', 'gender': 'female'},
    {'login': 'una', 'password': '000', 'name': 'Юна Цой', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            
            user_name = ''
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
        else:
            authorized = False
            login = ''
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, user_name=user_name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        return render_template('lab4/login.html', error='Не введён логин', login=login, authorized=False)
    
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', login=login, authorized=False)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, login=login, authorized=False)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge-form')
def fridge_form():
    return render_template('lab4/fridge-form.html')

@lab4.route('/lab4/fridge', methods=['POST'])
def fridge():
    temperature = request.form.get('temperature')
    
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    temperature = int(temperature)
    

    if temperature < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    
    if temperature > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    
    snowflakes = 0
    if -12 <= temperature <= -9:
        snowflakes = 3
    elif -8 <= temperature <= -5:
        snowflakes = 2
    elif -4 <= temperature <= -1:
        snowflakes = 1
    
    return render_template('lab4/fridge.html', temperature=temperature, snowflakes=snowflakes)

@lab4.route('/lab4/grain-form')
def grain_form():
    return render_template('lab4/grain-form.html')

@lab4.route('/lab4/grain', methods=['POST'])
def grain():
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    prices = {
        'barley': 12000,  # ячмень
        'oats': 8500,     # овёс
        'wheat': 9000,    # пшеница
        'rye': 15000      # рожь
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if not weight:
        return render_template('lab4/grain.html', error='Ошибка: не указан вес')
    
    weight = float(weight)
    
    if weight <= 0:
        return render_template('lab4/grain.html', error='Ошибка: вес должен быть больше 0')
    
    
    if weight > 100:
        return render_template('lab4/grain.html', error='Извините, такого объёма сейчас нет в наличии')
    
    price_per_ton = prices.get(grain_type)
    total_cost = weight * price_per_ton
    
    discount = 0
    if weight > 10:
        discount = total_cost * 0.10
        total_cost -= discount
    
    grain_name = grain_names.get(grain_type)
    
    return render_template('lab4/grain.html', 
                         grain_name=grain_name,
                         weight=weight,
                         total_cost=total_cost,
                         discount=discount,
                         has_discount=weight > 10)