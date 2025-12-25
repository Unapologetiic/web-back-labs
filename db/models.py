from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash


class users(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)

    user_articles = db.relationship('articles', backref='author', lazy=True)

class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer)


class warehouse_users(db.Model, UserMixin):
    __tablename__ = 'warehouse_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    group_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Связи
    orders = db.relationship('warehouse_orders', backref='user', lazy=True)

class warehouse_products(db.Model):
    __tablename__ = 'warehouse_products'
    
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    price = db.Column(db.Float, default=0.00, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    order_items = db.relationship('warehouse_order_items', backref='product', lazy=True)

class warehouse_orders(db.Model):
    __tablename__ = 'warehouse_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('warehouse_users.id'), nullable=False)
    status = db.Column(db.String(20), default='неоплачен')
    total_amount = db.Column(db.Float, default=0.00, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    items = db.relationship('warehouse_order_items', backref='order', lazy=True, cascade='all, delete-orphan')

class warehouse_order_items(db.Model):
    __tablename__ = 'warehouse_order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('warehouse_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('warehouse_products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)

def init_warehouse_data():
    """Инициализация базы данных"""
    db.create_all()
    
    # Проверяем, есть ли тестовый пользователь
    test_user = warehouse_users.query.filter_by(username='warehouse_manager').first()
    if not test_user:
        # Создаем тестового пользователя
        user = warehouse_users(
            username='warehouse_manager',
            password_hash=generate_password_hash('SecurePass123!'),
            full_name='Кудеярова Яна Олеговна',
            group_name='ФБИ-31',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
    
    # Проверяем, есть ли товары
    count = warehouse_products.query.count()
    if count < 100:  # Проверяем, меньше ли 100 товаров
        test_products = [
            # 1-30 (существующие товары)
            ('ART001', 'Холодильник Samsung', 15, 45000.00),
            ('ART002', 'Стиральная машина LG', 20, 32000.00),
            ('ART003', 'Посудомоечная машина Bosch', 10, 55000.00),
            ('ART004', 'Микроволновая печь Panasonic', 25, 12000.00),
            ('ART005', 'Электрическая плита Gorenje', 8, 28000.00),
            ('ART006', 'Кофемашина DeLonghi', 12, 35000.00),
            ('ART007', 'Пылесос Dyson', 18, 25000.00),
            ('ART008', 'Кондиционер Mitsubishi', 7, 42000.00),
            ('ART009', 'Блендер Philips', 30, 5000.00),
            ('ART010', 'Мультиварка Redmond', 22, 8000.00),
            ('ART011', 'Электрочайник Tefal', 35, 3000.00),
            ('ART012', 'Тостер Moulinex', 28, 4000.00),
            ('ART013', 'Кухонный комбайн Kenwood', 9, 15000.00),
            ('ART014', 'Мясорубка Zelmer', 14, 9000.00),
            ('ART015', 'Хлебопечка Scarlett', 11, 7000.00),
            ('ART016', 'Соковыжималка Braun', 16, 12000.00),
            ('ART017', 'Фен Rowenta', 40, 3500.00),
            ('ART018', 'Утюг Philips', 38, 4500.00),
            ('ART019', 'Пароочиститель Karcher', 6, 18000.00),
            ('ART020', 'Водонагреватель Ariston', 13, 22000.00),
            ('ART021', 'Вытяжка для кухни Elikor', 17, 15000.00),
            ('ART022', 'Посудомойка Electrolux', 5, 48000.00),
            ('ART023', 'Варочная панель Hansa', 19, 20000.00),
            ('ART024', 'Духовой шкаф Siemens', 8, 35000.00),
            ('ART025', 'Морозильная камера Liebherr', 4, 30000.00),
            ('ART026', 'Кофемолка Saeco', 21, 6000.00),
            ('ART027', 'Весы кухонные Beurer', 45, 2000.00),
            ('ART028', 'Аэрогриль Vitek', 15, 9000.00),
            ('ART029', 'Йогуртница Unit', 20, 3000.00),
            ('ART030', 'Сэндвичница Clatronic', 25, 2500.00),
            
            # 31-60 (новые товары - крупная техника)
            ('ART031', 'Двухдверный холодильник LG', 8, 65000.00),
            ('ART032', 'Стиральная машина с сушкой Samsung', 12, 45000.00),
            ('ART033', 'Встраиваемая посудомойка Siemens', 6, 68000.00),
            ('ART034', 'Микроволновка с грилем LG', 18, 15000.00),
            ('ART035', 'Индукционная варочная панель Bosch', 10, 35000.00),
            ('ART036', 'Робот-пылесос Xiaomi', 25, 22000.00),
            ('ART037', 'Кондиционер инверторный Daikin', 5, 58000.00),
            ('ART038', 'Электрическая духовка Electrolux', 9, 32000.00),
            ('ART039', 'Кухонный миксер KitchenAid', 14, 28000.00),
            ('ART040', 'Соковыжималка холодного отжима Hurom', 11, 35000.00),
            
            # 41-70 (новая техника для кухни)
            ('ART041', 'Электрическая мясорубка Philips', 16, 12000.00),
            ('ART042', 'Блендер стационарный Bosch', 20, 15000.00),
            ('ART043', 'Кофемолка автоматическая DeLonghi', 13, 18000.00),
            ('ART044', 'Электрический чайник с терморегулятором', 22, 6000.00),
            ('ART045', 'Тостер 4-х слотовый Tefal', 19, 7500.00),
            ('ART046', 'Вафельница Vitek', 25, 4500.00),
            ('ART047', 'Электрогриль Tefal', 14, 12000.00),
            ('ART048', 'Мультипекарь Redmond', 17, 9000.00),
            ('ART049', 'Йогуртница с таймером Scarlett', 21, 4000.00),
            ('ART050', 'Мороженица Unold', 8, 15000.00),
            
            # 51-80 (бытовая техника)
            ('ART051', 'Пароочиститель для одежды Philips', 15, 14000.00),
            ('ART052', 'Увлажнитель воздуха Boneco', 23, 12000.00),
            ('ART053', 'Очиститель воздуха Xiaomi', 18, 15000.00),
            ('ART054', 'Обогреватель инфракрасный Polaris', 30, 8000.00),
            ('ART055', 'Вентилятор напольный Vitek', 35, 5000.00),
            ('ART056', 'Ионизатор воздуха Maxion', 20, 7000.00),
            ('ART057', 'Электрический камин Real Flame', 6, 25000.00),
            ('ART058', 'Тепловая пушка Ballu', 12, 9000.00),
            ('ART059', 'Конвектор Electrolux', 16, 11000.00),
            ('ART060', 'Масляный обогреватель Scarlett', 25, 6000.00),
            
            # 61-90 (мелкая техника)
            ('ART061', 'Эпилятор Braun', 28, 12000.00),
            ('ART062', 'Массажер для шеи Xiaomi', 32, 5000.00),
            ('ART063', 'Электробритва Philips', 40, 9000.00),
            ('ART064', 'Триммер для бороды Moser', 35, 4500.00),
            ('ART065', 'Машинка для стрижки Wahl', 22, 8000.00),
            ('ART066', 'Зубная щетка электрическая Oral-B', 50, 7000.00),
            ('ART067', 'Ирригатор Waterpik', 18, 13000.00),
            ('ART068', 'Весы напольные Xiaomi', 45, 3000.00),
            ('ART069', 'Термометр инфракрасный Berrcom', 30, 4000.00),
            ('ART070', 'Тонометр автоматический Omron', 25, 6000.00),
            
            # 71-100 (техника для дома)
            ('ART071', 'Швейная машина Janome', 10, 25000.00),
            ('ART072', 'Оверлок Jaguar', 8, 32000.00),
            ('ART073', 'Паровой генератор Philips', 15, 18000.00),
            ('ART074', 'Отпариватель для одежды Tefal', 22, 9000.00),
            ('ART075', 'Сушилка для белья', 30, 7000.00),
            ('ART076', 'Утюг с парогенератором Tefal', 18, 22000.00),
            ('ART077', 'Пылесос с аквафильтром Karcher', 12, 35000.00),
            ('ART078', 'Робот-мойщик окон Hobot', 6, 45000.00),
            ('ART079', 'Аккумуляторный пылесос Dyson', 20, 40000.00),
            ('ART080', 'Пароочиститель для окон', 14, 12000.00),
            
            # 81-100 (техника для красоты)
            ('ART081', 'Фен-щетка Remington', 25, 8000.00),
            ('ART082', 'Стайлер для волос BaByliss', 20, 12000.00),
            ('ART083', 'Плойка для волос Rowenta', 18, 9000.00),
            ('ART084', 'Выпрямитель для волос Philips', 22, 11000.00),
            ('ART085', 'Бигуди электрические', 30, 5000.00),
            ('ART086', 'Массажная расческа', 40, 3000.00),
            ('ART087', 'Маникюрный набор Braun', 28, 15000.00),
            ('ART088', 'Пилка для ног электрическая', 35, 4000.00),
            ('ART089', 'Аппарат для чистки лица', 15, 18000.00),
            ('ART090', 'Солярий домашний', 4, 75000.00),
            
            # 91-110 (кухонная техника премиум)
            ('ART091', 'Кофемашина автоматическая Jura', 7, 120000.00),
            ('ART092', 'Винный шкаф Liebherr', 5, 85000.00),
            ('ART093', 'Пароварка Tefal', 12, 22000.00),
            ('ART094', 'Кухонный процессор Thermomix', 6, 150000.00),
            ('ART095', 'Вакууматор для продуктов', 20, 12000.00),
            ('ART096', 'Электрическая соковыжималка Omega', 10, 28000.00),
            ('ART097', 'Блинница Tefal', 25, 9000.00),
            ('ART098', 'Электрокастрюля-мультиварка', 18, 16000.00),
            ('ART099', 'Йогуртница на 7 баночек', 22, 6000.00),
            ('ART100', 'Мороженица с компрессором', 8, 35000.00)
        ]
        
        for article, name, quantity, price in test_products:
            # Проверяем, не существует ли уже товар с таким артикулом
            existing = warehouse_products.query.filter_by(article=article).first()
            if not existing:
                product = warehouse_products(
                    article=article,
                    name=name,
                    quantity=quantity,
                    price=price
                )
                db.session.add(product)
        
        db.session.commit()