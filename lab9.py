from flask import Blueprint, render_template, jsonify, request, session
import json
import random

lab9 = Blueprint('lab9', __name__, template_folder='templates')

# 10 подарков с PNG картинками
GIFTS = [
    {"id": 1, "name": "Подарок 1", "message": "С Новым годом! 🎄", "image": "gift1.jpg"},
    {"id": 2, "name": "Подарок 2", "message": "Удачи в учебе! 📚", "image": "gift2.png"},
    {"id": 3, "name": "Подарок 3", "message": "Крепкого здоровья! 💪", "image": "gift3.png"},
    {"id": 4, "name": "Подарок 4", "message": "Много счастья! 😊", "image": "gift4.png"},
    {"id": 5, "name": "Подарок 5", "message": "Успехов во всем! 🌟", "image": "gift5.png"},
    {"id": 6, "name": "Подарок 6", "message": "Верных друзей! 👫", "image": "gift6.png"},
    {"id": 7, "name": "Подарок 7", "message": "Интересных идей! 💡", "image": "gift7.png"},
    {"id": 8, "name": "Подарок 8", "message": "Финансового благополучия! 💰", "image": "gift8.png"},
    {"id": 9, "name": "Подарок 9", "message": "Путешествий и впечатлений! ✈️", "image": "gift9.png"},
    {"id": 10, "name": "Подарок 10", "message": "Уютного дома! 🏡", "image": "gift10.png"}
]

def generate_non_overlapping_positions():
    """Генерирует случайные позиции для 10 подарков без наложения"""
    positions = []
    grid_size = 6  # Сетка 6x6 для 10 подарков
    cell_width = 15  # 15% ширины
    cell_height = 15  # 15% высоты
    
    # Создаем сетку доступных позиций
    grid_cells = []
    for row in range(grid_size):
        for col in range(grid_size):
            left = 5 + col * cell_width
            top = 10 + row * cell_height
            grid_cells.append((left, top))
    
    # Выбираем 10 уникальных позиций
    random.shuffle(grid_cells)
    selected_cells = grid_cells[:10]
    
    for left, top in selected_cells:
        positions.append({"left": left, "top": top})
    
    return positions

@lab9.route('/lab9/')
def index():
    if 'gifts_state' not in session:
        # Перемешиваем порядок подарков
        shuffled_gifts = GIFTS.copy()
        random.shuffle(shuffled_gifts)
        
        # Генерируем позиции без наложения
        positions = generate_non_overlapping_positions()
        
        # Сохраняем состояние
        gifts_state = []
        for i, gift in enumerate(shuffled_gifts):
            gifts_state.append({
                "id": gift["id"],
                "name": gift["name"],
                "opened": False,
                "message": gift["message"],
                "image": gift["image"],
                "left": positions[i]["left"],
                "top": positions[i]["top"]
            })
        
        session['gifts_state'] = json.dumps(gifts_state, ensure_ascii=False)
        session['opened_count'] = 0
    
    gifts = json.loads(session['gifts_state'])
    opened_count = session.get('opened_count', 0)
    unopened_count = len([g for g in gifts if not g['opened']])
    
    return render_template('lab9/index.html', 
                         gifts=gifts,
                         opened_count=opened_count,
                         unopened_count=unopened_count)

@lab9.route('/lab9/open', methods=['POST'])
def open_gift():
    try:
        gift_id = request.json.get('id')
        
        if not gift_id:
            return jsonify({"error": "Нет ID подарка"}), 400
        
        # Получаем данные из сессии
        if 'gifts_state' not in session:
            return jsonify({"error": "Сессия не найдена"}), 400
        
        # Преобразуем строку JSON в список словарей
        gifts = json.loads(session['gifts_state'])
        opened_count = session.get('opened_count', 0)
        
        if opened_count >= 3:
            return jsonify({"error": "Вы уже открыли максимальное количество подарков (3)!"}), 400
        
        # Ищем подарок по ID
        for gift in gifts:
            if gift['id'] == gift_id:
                if gift['opened']:
                    return jsonify({"error": "Этот подарок уже открыт!"}), 400
                
                # Обновляем состояние
                gift['opened'] = True
                opened_count += 1
                
                # Сохраняем в сессию
                session['gifts_state'] = json.dumps(gifts, ensure_ascii=False)
                session['opened_count'] = opened_count
                session.modified = True
                
                # Формируем URL для картинки
                image_url = f"/static/lab9/{gift['image']}"
                
                # Считаем оставшиеся
                unopened_count = len([g for g in gifts if not g['opened']])
                
                return jsonify({
                    "success": True,
                    "message": gift['message'],
                    "image": image_url,
                    "opened_count": opened_count,
                    "unopened_count": unopened_count
                })
        
        return jsonify({"error": "Подарок не найден"}), 404
        
    except Exception as e:
        return jsonify({"error": f"Ошибка сервера: {str(e)}"}), 500

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    try:
        # Перемешиваем заново
        shuffled_gifts = GIFTS.copy()
        random.shuffle(shuffled_gifts)
        
        # Новые позиции без наложения
        positions = generate_non_overlapping_positions()
        
        gifts_state = []
        for i, gift in enumerate(shuffled_gifts):
            gifts_state.append({
                "id": gift["id"],
                "name": gift["name"],
                "opened": False,
                "message": gift["message"],
                "image": gift["image"],
                "left": positions[i]["left"],
                "top": positions[i]["top"]
            })
        
        session['gifts_state'] = json.dumps(gifts_state, ensure_ascii=False)
        session['opened_count'] = 0
        session.modified = True
        
        return jsonify({"success": True, "message": "Подарки перемешаны!"})
        
    except Exception as e:
        return jsonify({"error": f"Ошибка сброса: {str(e)}"}), 500