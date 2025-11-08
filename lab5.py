from flask import Blueprint, render_template, request, make_response, redirect

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', username="anonymous")

@lab5.route('/lab5/login')
def login():
    return "Страница входа - здесь будет форма входа"

@lab5.route('/lab5/register')
def register():
    return "Страница регистрации - здесь будет форма регистрации"

@lab5.route('/lab5/list')
def list():
    return "Список статей - здесь будут отображаться статьи"

@lab5.route('/lab5/create')
def create():
    return "Создание статьи - здесь будет форма для создания статьи"