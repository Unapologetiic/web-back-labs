from flask import Blueprint, render_template, jsonify, request, session
import random

lab9 = Blueprint('lab9', __name__, template_folder='templates')


GIFTS = [
    {"id": 1, "name": "Подарок 1", "message": "С Новым годом! 🎄 Пусть этот год принесет вам много радости и счастья!", "image": "gift1.jpg", "auth_required": False},
    {"id": 2, "name": "Подарок 2", "message": "Удачи в учебе! 📚 Пусть знания даются легко, а экзамены сдаются на отлично!", "image": "gift2.png", "auth_required": False},
    {"id": 3, "name": "Подарок 3", "message": "Крепкого здоровья! 💪 Пусть каждый день приносит бодрость и хорошее настроение!", "image": "gift3.png", "auth_required": True},
    {"id": 4, "name": "Подарок 4", "message": "Много счастья! 😊 Пусть ваша жизнь будет наполнена улыбками и теплом близких!", "image": "gift4.png", "auth_required": False},
    {"id": 5, "name": "Подарок 5", "message": "Успехов во всем! 🌟 Пусть любое начинание завершается победой!", "image": "gift5.png", "auth_required": False},
    {"id": 6, "name": "Подарок 6", "message": "Верных друзей! 👫 Пусть рядом всегда будут те, кто поддержит в трудную минуту!", "image": "gift6.png", "auth_required": True},
    {"id": 7, "name": "Подарок 7", "message": "Интересных идей! 💡 Пусть творчество и вдохновение никогда не покидают вас!", "image": "gift7.png", "auth_required": False},
    {"id": 8, "name": "Подарок 8", "message": "Финансового благополучия! 💰 Пусть ваш кошелек всегда будет полон!", "image": "gift8.png", "auth_required": True},
    {"id": 9, "name": "Подарок 9", "message": "Путешествий и впечатлений! ✈️ Пусть каждый день открывает новые горизонты!", "image": "gift9.png", "auth_required": False},
    {"id": 10, "name": "Подарок 10", "message": "Уютного дома! 🏡 Пусть ваш дом всегда будет наполнен теплом и уютом!", "image": "gift10.png", "auth_required": True}
]

# Глобальные хранилища в памяти сервера
# Ключ: session_id, значение: данные пользователя
gifts_state_storage = {}
user_opened_count = {}

def get_session_id():
    """Получает уникальный идентификатор сессии"""
    if 'user_id' in session:
        return f"user_{session['user_id']}"
    else:
        return f"guest_{session.get('_id', 'anonymous')}"

def init_user_session():
    """Инициализирует состояние подарков для пользователя"""
    session_id = get_session_id()
    
    if session_id not in gifts_state_storage:
        # Перемешиваем подарки в случайном порядке
        shuffled_gifts = GIFTS.copy()
        random.shuffle(shuffled_gifts)
        
        # Генерируем случайные позиции для 10 подарков
        # Позиции сохраняются при каждом обновлении страницы
        positions = []
        used_positions = set()
        
        for _ in range(10):
            while True:
                left = random.randint(5, 85)  # Отступ от левого края 5-85%
                top = random.randint(10, 70)  # Отступ от верхнего края 10-70%
                position_key = f"{left}_{top}"
                
                # Проверяем, чтобы подарки не перекрывались сильно
                too_close = False
                for pos in positions:
                    if abs(pos['left'] - left) < 15 and abs(pos['top'] - top) < 15:
                        too_close = True
                        break
                
                if not too_close and position_key not in used_positions:
                    used_positions.add(position_key)
                    positions.append({"left": left, "top": top})
                    break
        
        # Сохраняем состояние подарков для пользователя
        user_gifts = []
        for i, gift in enumerate(shuffled_gifts):
            user_gifts.append({
                "id": gift["id"],
                "name": gift["name"],
                "opened": False,
                "message": gift["message"],
                "image": gift["image"],
                "auth_required": gift["auth_required"],
                "left": positions[i]["left"],
                "top": positions[i]["top"],
                "available": True,
                "tooltip": ""
            })
        
        gifts_state_storage[session_id] = user_gifts
        user_opened_count[session_id] = 0
    
    return session_id

def is_authenticated():
    """Проверяет, авторизован ли пользователь"""
    return 'user_id' in session

def get_username():
    """Возвращает имя пользователя"""
    return session.get('login', 'Гость')

@lab9.route('/lab9/')
def index():
    session_id = init_user_session()
    
    gifts = gifts_state_storage[session_id]
    opened = user_opened_count.get(session_id, 0)
    unopened = len([g for g in gifts if not g['opened']])
    
    # Проверяем авторизацию
    authenticated = is_authenticated()
    username = get_username()
    
    # Устанавливаем доступность подарков
    for gift in gifts:
        if gift['auth_required'] and not authenticated:
            gift['available'] = False
            gift['tooltip'] = "Требуется авторизация"
        else:
            gift['available'] = True
            gift['tooltip'] = "Нажмите, чтобы открыть"
    
    return render_template('lab9/index.html', 
                         gifts=gifts,
                         opened_count=opened,
                         unopened_count=unopened,
                         username=username,
                         authenticated=authenticated)

@lab9.route('/lab9/open', methods=['POST'])
def open_gift():
    try:
        data = request.get_json()
        gift_id = data.get('id')
        
        if not gift_id:
            return jsonify({"error": "Не указан ID подарка"}), 400
        
        session_id = get_session_id()
        authenticated = is_authenticated()
        
        if session_id not in gifts_state_storage:
            return jsonify({"error": "Сессия не найдена"}), 400
        
        gifts = gifts_state_storage[session_id]
        opened = user_opened_count.get(session_id, 0)
        
        # Проверяем, не открыл ли пользователь уже 3 подарка
        if opened >= 3:
            return jsonify({"error": "Вы уже открыли максимальное количество подарков (3)!"}), 400
        
        # Ищем подарок по ID
        for gift in gifts:
            if gift['id'] == gift_id:
                if gift['opened']:
                    return jsonify({"error": "Этот подарок уже открыт!"}), 400
                
                # Проверяем доступность для авторизованных пользователей
                if gift['auth_required'] and not authenticated:
                    return jsonify({
                        "error": "Этот подарок доступен только авторизованным пользователям!",
                        "auth_required": True
                    }), 403
                
                # Открываем подарок
                gift['opened'] = True
                opened += 1
                
                # Сохраняем состояние
                user_opened_count[session_id] = opened
                
                # Считаем оставшиеся подарки
                unopened = len([g for g in gifts if not g['opened']])
                
                return jsonify({
                    "success": True,
                    "message": gift['message'],
                    "image": f"/static/lab9/{gift['image']}",
                    "opened_count": opened,
                    "unopened_count": unopened
                })
        
        return jsonify({"error": "Подарок не найден"}), 404
        
    except Exception as e:
        return jsonify({"error": f"Ошибка сервера: {str(e)}"}), 500

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    """Сброс игры - только для авторизованных пользователей"""
    if not is_authenticated():
        return jsonify({"error": "Требуется авторизация для использования функции 'Дед Мороз'"}), 401
    
    try:
        session_id = get_session_id()
        
        # Перемешиваем подарки заново
        shuffled_gifts = GIFTS.copy()
        random.shuffle(shuffled_gifts)
        
        # Генерируем новые случайные позиции
        positions = []
        used_positions = set()
        
        for _ in range(10):
            while True:
                left = random.randint(5, 85)
                top = random.randint(10, 70)
                position_key = f"{left}_{top}"
                
                too_close = False
                for pos in positions:
                    if abs(pos['left'] - left) < 15 and abs(pos['top'] - top) < 15:
                        too_close = True
                        break
                
                if not too_close and position_key not in used_positions:
                    used_positions.add(position_key)
                    positions.append({"left": left, "top": top})
                    break
        
        # Создаем новые подарки
        user_gifts = []
        for i, gift in enumerate(shuffled_gifts):
            user_gifts.append({
                "id": gift["id"],
                "name": gift["name"],
                "opened": False,
                "message": gift["message"],
                "image": gift["image"],
                "auth_required": gift["auth_required"],
                "left": positions[i]["left"],
                "top": positions[i]["top"],
                "available": True,
                "tooltip": ""
            })
        
        # Сбрасываем состояние
        gifts_state_storage[session_id] = user_gifts
        user_opened_count[session_id] = 0
        
        return jsonify({
            "success": True, 
            "message": "🎅 Дед Мороз наполнил все коробки заново! 🎁"
        })
        
    except Exception as e:
        return jsonify({"error": f"Ошибка сброса: {str(e)}"}), 500