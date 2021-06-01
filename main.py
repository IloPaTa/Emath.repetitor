import os
import sqlite3

from flask import Flask, render_template, request, g, flash, url_for
from flask_login import LoginManager, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from Login import UserLogin

from DB import DB

DATABASE = 'users.db'
SECRET_KEY = 'f23wefdsfe>FSFS?F'
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'users.db')))
login_manager = LoginManager(app)


# Тут вся работа с БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DB(db)


def create_db():
    db = connect_db()
    with app.open_resource('db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Тут вся работа с Авторизацией
@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


@app.route('/calculations', methods=['post', 'get'])
def calculations():
    ans1 = ""
    ans2 = ""
    if request.method == 'POST':
        ans1 = request.form.get('task1')
        ans2 = request.form.get('task2')

    return render_template('calculations.html', ans1=ans1, ans2=ans2)


@app.route('/degrees_and_roots', methods=['post', 'get'])
def degrees_and_roots():
    ans1 = ""
    ans2 = ""
    ans3 = ""
    ans4 = ""
    ans5 = ""
    ans6 = ""
    ans7 = ""
    if request.method == 'POST':
        ans1 = request.form.get('task1')
        ans2 = request.form.get('task2')
        ans3 = request.form.get('task3')
        ans4 = request.form.get('task4')
        ans5 = request.form.get('task5')
        ans6 = request.form.get('task6')
        ans7 = request.form.get('task7')
    return render_template('degrees_and_roots.html', task1=ans1, task2=ans2, task3=ans3, task4=ans4, task5=ans5,
                           task6=ans6, task7=ans7)


@app.route('/FSY', methods=['post', 'get'])
def fsy():
    ans1 = ""
    ans2 = ""
    ans3 = ""
    if request.method == 'POST':
        ans1 = request.form.get('task1')
        ans2 = request.form.get('task2')
        ans3 = request.form.get('task3')
    return render_template('FSY.html', ans1=ans1, ans2=ans2, ans3=ans3)


@app.route('/lineal', methods=['post', 'get'])
def lineal():
    ans1 = ""
    if request.method == 'POST':
        ans1 = request.form.get('task1')
    return render_template('lineal.html', ans1=ans1)


@app.route('/quadratic', methods=['post', 'get'])
def quadratic():
    ans1 = ""
    ans2 = ""
    ans3 = ""
    ans4 = ""
    ans5 = ""
    ans6 = ""
    ans7 = ""
    ans8 = ""
    if request.method == 'POST':
        ans1 = request.form.get('task1')
        ans2 = request.form.get('task2')
        ans3 = request.form.get('task3')
        ans4 = request.form.get('task4')
        ans5 = request.form.get('task5')
        ans6 = request.form.get('task6')
        ans7 = request.form.get('task7')
        ans8 = request.form.get('task8')
    return render_template('quadratic.html', task1=ans1, task2=ans2, task3=ans3, task4=ans4, task5=ans5,
                           task6=ans6, task7=ans7, task8=ans8)


@app.route('/drobi', methods=['post', 'get'])
def drobi():
    ans1 = ""
    ans2 = ""
    ans3 = ""
    ans4 = ""
    ans5 = ""
    ans6 = ""
    ans7 = ""
    if request.method == 'POST':
        ans1 = request.form.get('task1')
        ans2 = request.form.get('task2')
        ans3 = request.form.get('task3')
        ans4 = request.form.get('task4')
        ans5 = request.form.get('task5')
        ans6 = request.form.get('task6')
        ans7 = request.form.get('task7')
    return render_template('drobi.html', task1=ans1, task2=ans2, task3=ans3, task4=ans4, task5=ans5,
                           task6=ans6, task7=ans7)


@app.route('/linner', methods=['post', 'get'])
def linner():
    ans1 = ""
    if request.method == 'POST':
        ans1 = request.form.get('task1')
    return render_template('linner.html', task1=ans1)


@app.route('/')
@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('calculations'))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html")


@app.route('/register', methods=['post', 'get'])
def register():
    if request.method == 'POST':
        hash = generate_password_hash(request.form['psw'])
        res = dbase.addUser(request.form['name'], request.form['mail'], hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(port=5000
            , host='127.0.0.1')
