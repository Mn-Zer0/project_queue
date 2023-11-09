from flask import Flask, render_template, Response, request, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from database import login_check, add_user
from user_login import User
import sys


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print(user_id, file=sys.stderr)
    return User().fromDB(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    # recs = get_users()
    if request.method == "POST":
        if request.form.get('queue'):
            return render_template('index.html', error="YES")
    return render_template('index.html')  # , user1=recs[0], user2=recs[1], user3=recs[2], user4=recs[3])


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('login'):
            username = request.form.get('username')
            password = request.form.get('password')

            if not username:
                return render_template('login.html', error="Логин не введён")
            if not password:
                return render_template('login.html', error="Пароль не введён")

            responce = login_check(username, password)
            if not login_check(username, password):
                return render_template('login.html', error="Пользователя не существует")
            else:
                userlogin = User().create(responce)
                login_user(userlogin)
                return redirect('/')

        elif request.form.get('registration'):
            return redirect('/registration/')
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        second_name = request.form.get('second_name')
        log1n = request.form.get('login')
        password = request.form.get('password')
        if not name:
            return render_template('registration.html', error="Пожалуйста введите имя")
        if not second_name:
            return render_template('registration.html', error=second_name)
        if not log1n:
            return render_template('registration.html', error="Пожалуйста введите логин")
        if not password:
            return render_template('registration.html', error="Пожалуйста введите пароль")

        print(name, second_name, log1n, password, file=sys.stderr)
        add_user(log1n, password, name, second_name)
        return redirect('/login/')
    return render_template('registration.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
