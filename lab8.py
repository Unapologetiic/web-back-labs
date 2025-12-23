from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
import datetime

lab8 = Blueprint('lab8', __name__, template_folder='templates')

# Декоратор для проверки авторизации
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/lab8/login')
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Главная страница
@lab8.route('/lab8/')
def lab():
    if 'user_id' in session:
        user = users.query.get(session['user_id'])
        if user:
            username = user.login
            login = user.login
            user_count = users.query.count()
            article_count = articles.query.filter_by(login_id=user.id).count()
        else:
            session.clear()
            username = 'anonymous'
            login = None
            user_count = None
            article_count = None
    else:
        username = 'anonymous'
        login = None
        user_count = None
        article_count = None
    
    return render_template('lab8/lab8.html', 
                         username=username, 
                         login=login,
                         user_count=user_count,
                         article_count=article_count)

# Регистрация
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form or not password_form:
        return render_template('lab8/register.html', 
                             error='Логин и пароль не должны быть пустыми')
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                             error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    db.session.add(new_user)
    db.session.commit()
    
    session['user_id'] = new_user.id
    session['login'] = new_user.login
    
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'  # Добавляем обработку галочки
    
    if not login_form or not password_form:
        return render_template('lab8/login.html', 
                             error='Логин и пароль не должны быть пустыми')
    
    user = users.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        session['user_id'] = user.id
        session['login'] = user.login
        
    
        if remember:
            session.permanent = True
            
        else:
            session.permanent = False 
        
        print(f"Пользователь {user.login} вошел. Запомнить: {remember}")
        
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', 
                         error='Ошибка входа: неверный логин или пароль')

# Выход
@lab8.route('/lab8/logout')
@login_required
def logout():
    print(f"Пользователь {session.get('login')} выходит")
    session.clear()
    return redirect('/lab8/')

# Остальные функции без изменений
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_id = session['user_id']
    user_articles = articles.query.filter_by(login_id=user_id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/create.html', 
                             error='Заголовок и текст статьи не должны быть пустыми')
    
    new_article = articles(
        login_id=session['user_id'],
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    user_id = session['user_id']
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != user_id:
        return "У вас нет прав для редактирования этой статьи", 403
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/edit.html', 
                             article=article,
                             error='Заголовок и текст статьи не должны быть пустыми')
    
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    user_id = session['user_id']
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != user_id:
        return "У вас нет прав для удаления этой статьи", 403
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/public')
def public_articles():
    # Получаем все публичные статьи, отсортированные по убыванию лайков
    public_articles_list = articles.query.filter_by(is_public=True).order_by(articles.likes.desc()).all()
    
    # Получаем имя пользователя для отображения в шаблоне
    username = 'anonymous'
    if 'user_id' in session:
        user = users.query.get(session['user_id'])
        if user:
            username = user.login
    
    return render_template('lab8/public.html', 
                         articles=public_articles_list,
                         username=username)


# Поиск по статьям
@lab8.route('/lab8/search', methods=['GET', 'POST'])
def search_articles():
    search_results = []
    search_query = ""
    
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        
        if search_query:
            # Регистронезависимый поиск в заголовке и тексте статей
            if 'user_id' in session:
                user_id = session['user_id']
                # Для авторизованных: свои статьи + публичные статьи других пользователей
                search_results = articles.query.filter(
                    db.or_(
                        db.and_(
                            articles.login_id == user_id,
                            db.or_(
                                articles.title.ilike(f'%{search_query}%'),
                                articles.article_text.ilike(f'%{search_query}%')
                            )
                        ),
                        db.and_(
                            articles.is_public == True,
                            articles.login_id != user_id,
                            db.or_(
                                articles.title.ilike(f'%{search_query}%'),
                                articles.article_text.ilike(f'%{search_query}%')
                            )
                        )
                    )
                ).all()
            else:
                # Для неавторизованных: только публичные статьи
                search_results = articles.query.filter(
                    articles.is_public == True,
                    db.or_(
                        articles.title.ilike(f'%{search_query}%'),
                        articles.article_text.ilike(f'%{search_query}%')
                    )
                ).all()
    
    # Получаем имя пользователя для шаблона
    username = 'anonymous'
    if 'user_id' in session:
        user = users.query.get(session['user_id'])
        if user:
            username = user.login
    
    return render_template('lab8/search.html',
                         search_results=search_results,
                         search_query=search_query,
                         username=username)


@lab8.route('/lab8/like/<int:article_id>', methods=['POST'])  
def like_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    # Проверяем, что статья публичная
    if not article.is_public:
        return "Эта статья не публичная", 403
    
    article.likes += 1
    db.session.commit()
    
    return redirect('/lab8/public')