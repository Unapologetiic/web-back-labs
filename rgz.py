from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import warehouse_users, warehouse_products, warehouse_orders, warehouse_order_items
import json
from datetime import datetime

rgz = Blueprint('rgz', __name__, template_folder='templates')

# Декоратор для проверки авторизации
def warehouse_login_required(f):
    def wrapper(*args, **kwargs):
        if 'warehouse_user_id' not in session:
            return redirect('/rgz')
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper



@rgz.route('/rgz')
def index():
    """Главная страница RGZ"""
    return render_template('rgz/index.html')

@rgz.route('/rgz/products')
@warehouse_login_required
def products():
    """Страница управления товарами"""
    return render_template('rgz/products.html')

@rgz.route('/rgz/orders')
@warehouse_login_required
def orders():
    """Страница управления заказами"""
    return render_template('rgz/orders.html')

@rgz.route('/rgz/cart')
@warehouse_login_required
def cart():
    """Страница корзины"""
    return render_template('rgz/cart.html')

@rgz.route('/rgz/profile')
@warehouse_login_required
def profile():
    """Страница профиля"""
    return render_template('rgz/profile.html')



@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return render_template('rgz/login.html', 
                             error='Логин и пароль не должны быть пустыми')
    
    user = warehouse_users.query.filter_by(username=username, is_active=True).first()
    
    if user and check_password_hash(user.password_hash, password):
        session['warehouse_user_id'] = user.id
        session['warehouse_username'] = user.username
        session['warehouse_full_name'] = user.full_name
        session['warehouse_group'] = user.group_name
        
        return redirect('/rgz')  # Редирект на главную после входа
    
    return render_template('rgz/login.html', 
                         error='Ошибка входа: неверный логин или пароль')

# Выход
@rgz.route('/rgz/logout')
@warehouse_login_required
def logout():
    session.pop('warehouse_user_id', None)
    session.pop('warehouse_username', None)
    session.pop('warehouse_full_name', None)
    session.pop('warehouse_group', None)
    return redirect('/rgz')

#Получить товары с пагинацией (50 на страницу)
@rgz.route('/rgz/api/products')
@warehouse_login_required
def api_get_products():
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Фиксировано 50 товаров на страницу
    
    offset = (page - 1) * per_page
    products = warehouse_products.query.order_by(warehouse_products.id)\
                                      .offset(offset)\
                                      .limit(per_page)\
                                      .all()
    
    total = warehouse_products.query.count()
    
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'article': product.article,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
        })
    
    return jsonify({
        'products': products_list,
        'has_next': (offset + len(products)) < total,
        'page': page,
        'total': total
    })

@rgz.route('/rgz/api/products', methods=['POST'])
@warehouse_login_required
def api_add_product():
    try:
        article = request.form.get('article', '').strip()
        name = request.form.get('name', '').strip()
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))
        
        # Валидация
        if not article or not name:
            return jsonify({'error': 'Артикул и название обязательны'}), 400
        
        if quantity < 0:
            return jsonify({'error': 'Количество не может быть отрицательным'}), 400
        
        if price < 0:
            return jsonify({'error': 'Цена не может быть отрицательной'}), 400
        
        # Проверяем, существует ли товар
        existing_product = warehouse_products.query.filter_by(article=article).first()
        
        if existing_product:
            # Обновляем количество, цену И название 
            existing_product.quantity += quantity
            existing_product.price = price
            # Обновляем название при изменении
            if existing_product.name != name:
                existing_product.name = name
            message = f'Товар обновлен (добавлено {quantity} шт.)'
        else:
            # Создаем новый товар
            product = warehouse_products(
                article=article,
                name=name,
                quantity=quantity,
                price=price
            )
            db.session.add(product)
            message = 'Товар добавлен'
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Удалить товар
@rgz.route('/rgz/api/products/<int:product_id>', methods=['DELETE'])
@warehouse_login_required
def api_delete_product(product_id):
    try:
        product = warehouse_products.query.get_or_404(product_id)
        
        # Проверяем, есть ли товар в любых заказах
        order_items = warehouse_order_items.query.filter_by(product_id=product_id).first()
        
        if order_items:
            # Товар есть в заказах - нельзя удалить физически
            # Обнуляем количество и помечаем как недоступный
            product.quantity = 0
            
            # Добавляем префикс к названию, если нужно
            if not product.name.startswith("[СНЯТО С ПРОДАЖИ]"):
                product.name = f"[СНЯТО С ПРОДАЖИ] {product.name}"
            
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Товар есть в истории заказов. Количество обнулено, ' +
                          'товар помечен как снятый с продажи.'
            })
        
        # Если товара нет в заказах - удаляем полностью
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Товар удален'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Получить корзину из сессии
@rgz.route('/rgz/api/cart')
@warehouse_login_required
def api_get_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = warehouse_products.query.get(product_id)
        
        if product and quantity > 0:
            if quantity > product.quantity:
                quantity = product.quantity  # Нельзя взять больше, чем есть
                cart[product_id_str] = quantity
            
            item_total = quantity * product.price if product.price else 0
            total += item_total
            
            cart_items.append({
                'id': product.id,
                'article': product.article,
                'name': product.name,
                'quantity': quantity,
                'available': product.quantity,
                'price': product.price,
                'total': item_total
            })
    
    session['cart'] = cart
    
    return jsonify({
        'items': cart_items,
        'total': total,
        'count': len(cart_items)
    })

#Добавить товар в корзину
@rgz.route('/rgz/api/cart', methods=['POST'])
@warehouse_login_required
def api_add_to_cart():
    try:
        product_id = int(request.form.get('product_id', 0))
        quantity = int(request.form.get('quantity', 1))
        
        if not product_id or quantity <= 0:
            return jsonify({'error': 'Некорректные данные'}), 400
        
        product = warehouse_products.query.get_or_404(product_id)
        
        if quantity > product.quantity:
            return jsonify({'error': f'Недостаточно товара. Доступно: {product.quantity}'}), 400
        
        if 'cart' not in session:
            session['cart'] = {}
        
        cart = session['cart']
        current_qty = cart.get(str(product_id), 0)
        new_qty = current_qty + quantity
        
        if new_qty > product.quantity:
            return jsonify({'error': f'Недостаточно товара. Доступно: {product.quantity}'}), 400
        
        cart[str(product_id)] = new_qty
        session['cart'] = cart
        
        return jsonify({'success': True, 'quantity': new_qty})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Удалить из корзины
@rgz.route('/rgz/api/cart/<int:product_id>', methods=['DELETE'])
@warehouse_login_required
def api_remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        if str(product_id) in cart:
            del cart[str(product_id)]
            session['cart'] = cart
    
    return jsonify({'success': True})

# Очистить корзину
@rgz.route('/rgz/api/cart/clear', methods=['DELETE'])
@warehouse_login_required
def api_clear_cart():
    session.pop('cart', None)
    return jsonify({'success': True})

# Создать заказ из корзины
@rgz.route('/rgz/api/orders', methods=['POST'])
@warehouse_login_required
def api_create_order():
    try:
        if 'cart' not in session or not session['cart']:
            return jsonify({'error': 'Корзина пуста'}), 400
        
        cart = session['cart']
        user_id = session['warehouse_user_id']
        total_amount = 0
        
        # Создаем заказ
        order = warehouse_orders(
            user_id=user_id,
            status='неоплачен',
            total_amount=0
        )
        db.session.add(order)
        db.session.flush()  # Получаем ID заказа
        
        # Добавляем товары в заказ
        for product_id_str, quantity in cart.items():
            product_id = int(product_id_str)
            product = warehouse_products.query.get(product_id)
            
            if not product or product.quantity < quantity:
                db.session.rollback()
                return jsonify({'error': f'Недостаточно товара: {product.name if product else product_id}'}), 400
            
            # Добавляем элемент заказа
            order_item = warehouse_order_items(
                order_id=order.id,
                product_id=product_id,
                quantity=quantity,
                price_at_order=product.price
            )
            db.session.add(order_item)
            
            # Вычисляем общую сумму
            total_amount += quantity * product.price
        
        # Обновляем общую сумму заказа
        order.total_amount = total_amount
        
        # Очищаем корзину
        session.pop('cart', None)
        
        db.session.commit()
        return jsonify({'success': True, 'order_id': order.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#Получить список заказов
@rgz.route('/rgz/api/orders')
@warehouse_login_required
def api_get_orders():
    try:
        user_id = session['warehouse_user_id']
        user_orders = warehouse_orders.query.filter_by(user_id=user_id)\
                                           .order_by(warehouse_orders.created_at.desc())\
                                           .all()
        
        orders_list = []
        for order in user_orders:
            # Получаем количество товаров в заказе
            items_count = warehouse_order_items.query.filter_by(order_id=order.id).count()
            
            orders_list.append({
                'id': order.id,
                'status': order.status,
                'total_amount': order.total_amount,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'items_count': items_count
            })
        
        return jsonify({'orders': orders_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Оплатить заказ
@rgz.route('/rgz/api/orders/<int:order_id>/pay', methods=['POST'])
@warehouse_login_required
def api_pay_order(order_id):
    try:
        order = warehouse_orders.query.get_or_404(order_id)
        
        if order.status == 'оплачен':
            return jsonify({'error': 'Заказ уже оплачен'}), 400
        
        # Получаем товары из заказа
        order_items = warehouse_order_items.query.filter_by(order_id=order_id).all()
        
        # Проверяем наличие товаров и уменьшаем их количество
        for item in order_items:
            product = warehouse_products.query.get(item.product_id)
            
            if product.quantity < item.quantity:
                return jsonify({'error': f'Недостаточно товара: {product.name}'}), 400
            
            product.quantity -= item.quantity
        
        # Меняем статус заказа
        order.status = 'оплачен'
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#Удалить аккаунт
@rgz.route('/rgz/api/profile/delete', methods=['POST'])
@warehouse_login_required
def api_delete_account():
    try:
        user_id = session['warehouse_user_id']
        password = request.form.get('password', '')
        
        user = warehouse_users.query.get(user_id)
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Неверный пароль'}), 401
        
        # Проверяем, нет ли активных заказов у пользователя
        active_orders = warehouse_orders.query.filter_by(user_id=user_id, status='неоплачен').first()
        if active_orders:
            return jsonify({'error': 'Невозможно удалить аккаунт: есть неоплаченные заказы'}), 400
        
        # Деактивируем аккаунт 
        user.is_active = False
        db.session.commit()
        
        # Выходим из системы
        session.clear()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500