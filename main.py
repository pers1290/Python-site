import os
from flask import Flask, request, redirect, render_template, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send
import sqlite3
from dotenv import load_dotenv
from mail import send_mail
import random

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = '5457fae2a71f9331bf4bf3dd6813f90abeb33839f4608755ce301b9321c6'
socketio = SocketIO(app)
UPLOAD_FOLDER = 'static/avatar/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

FON_LIST = {'1': '/static/fon_img/fon_1.jpg', '2': '/static/fon_img/fon_2.jpg', '3': '/static/fon_img/fon_3.jpg',
            '4': '/static/fon_img/fon_12.gif', '5': '/static/fon_img/fon_5.gif', '6': '/static/fon_img/fon_6.jpg',
            '7': '/static/fon_img/fon_7.png', '8': '/static/fon_img/fon_8.jpg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return redirect("/tinttye")


@app.route('/exit')
def exit():
    session.clear()
    return redirect("/tinttye")


@app.route('/test_1')
def test_1():
    if 'name' not in session:
        session['error'] = 'Авторизируйтесь!'
        return redirect("/tinttye")
    return redirect("/change_fon")


@app.route('/test_2')
def test_2():
    if 'name' not in session:
        session['error'] = 'Авторизируйтесь!'
        return redirect("/tinttye")
    return redirect("/messenger")


@app.route('/tinttye', methods=['POST', 'GET'])
def tinttye():
    fon = '/static/fon_img/fon_7.png'
    name = ''
    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error')
    avatar = 'static/img_2/profil.png'
    connection = sqlite3.connect('db2/User_2.db')
    cursor = connection.cursor()
    session.permanent = True
    if 'name' in session:
        name = session['name']
    if 'fon' in session:
        fon = session['fon']
    if 'avatar' in session:
        avatar = session['avatar']
    if request.method == 'GET':
        cursor.execute('SELECT * FROM Users')
        users = cursor.fetchall()
        len_db = len(users)
        index_list = list(range(len_db))
        connection.commit()
        connection.close()
        return render_template('main.html', file_list=users, index_list=index_list, fon=fon, avatar=avatar, name=name,
                               error=error, s='')
    elif request.method == 'POST':
        answer_1 = request.form.get('user')
        answer_1 = answer_1.title()
        posts = cursor.execute('SELECT * FROM Users WHERE name = ?', (answer_1,)).fetchall()
        print(posts)
        len_db = len(posts)
        index_list = list(range(len_db))
        connection.commit()
        connection.close()
        return render_template('main.html', file_list=posts, index_list=index_list, fon=fon, avatar=avatar, name=name,
                               error=error, s='сброс')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    error_1 = ''
    error_2 = ''
    value_1, value_2, value_3 = '', '', ''
    system_error = ''
    if request.method == 'GET':
        if 'name' not in session:
            return render_template('registration.html', error_1=error_1, error_2=error_2,
                                   system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3)
        else:
            return redirect("/personal_account")
    elif request.method == 'POST':
        answer_1 = request.form.get('firstname')
        answer_2 = request.form.get('email')
        answer_3 = request.form.get('pasvord')
        answer_1 = answer_1.title()
        value_1, value_2, value_3 = answer_1, answer_3, answer_2
        connection = sqlite3.connect('db2/Reg_1.db')
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT name, password, phone, profil_img, fon_img FROM Reg WHERE name = ?', (answer_1,))
            users = cursor.fetchall()
            user = users[0]
            if check_password_hash(user[1], answer_3) is False:
                error_2 = 'Неверный пароль'
                return render_template('registration.html', error_1=error_1, error_2=error_2,
                                       system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3)
            session.permanent = True
            session['avatar'] = user[3]
            session['fon'] = user[4]
            connection.commit()
            connection.close()
            session['name'] = answer_1
            return redirect("/personal_account")
        except:
            system_error = 'Вас не в системе, зарегистрируйтесь'
            return render_template('registration.html', error_1=error_1, error_2=error_2,
                                   system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3)


@app.route('/change_fon', methods=['POST', 'GET'])
def change_fon():
    global FON_LIST
    session.permanent = True
    error = ''
    if request.method == 'GET':
        return render_template('change_fon.html', error=error, avatar=session['avatar'])
    elif request.method == 'POST':
        number = request.form.get('email')
        if number not in ('1', '2', '3', '4', '5', '6', '7', '8'):
            error = 'Может быть 1, 2 3...8'
            return render_template('change_fon.html', error=error)
        session['fon'] = FON_LIST[number]
        connection = sqlite3.connect('db2/Reg_1.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE Reg SET fon_img = ? WHERE name = ?', (session['fon'], session['name']))
        connection.commit()
        connection.close()
        return redirect("/tinttye")


@app.route('/login', methods=['POST', 'GET'])
def login():
    session.permanent = True
    avatar = 'static/img_2/profil.png'
    fon = '/static/fon_img/fon_1.jpg'
    error_1, error_2, error_3, error_4 = '', '', '', ''
    value_1, value_2, value_3, value_4 = '', '', '', ''
    system_error = ''
    if request.method == 'GET':
        return render_template('registr.html', error_1=error_1, error_2=error_2, error_3=error_3, error_4=error_4,
                               system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3,
                               value_4=value_4)
    elif request.method == 'POST':
        answer_1 = request.form.get('firstname')
        answer_2 = request.form.get('email')
        answer_3 = request.form.get('pasvord')
        answer_4 = request.form.get('pasvord2')
        answer_1 = answer_1.title()
        value_1, value_2, value_3, value_4 = answer_1, answer_3, answer_4, answer_2
        connection = sqlite3.connect('db2/Reg_1.db')
        cursor = connection.cursor()
        if answer_4 != answer_3:
            error_2 = 'Пароли не совпадают'
            error_3 = 'Пароли не совпадают'
        try:
            cursor.execute('SELECT password FROM Reg WHERE name = ?', (answer_1,))
            name_user = cursor.fetchall()
            if check_password_hash(name_user[0][0], answer_3):
                system_error = 'Вы уже зарегистрированы в системе'
            else:
                error_1 = 'Такой никнейм есть, придумайте новый'
        except:
            pass
        if (error_1, error_2, error_3, error_4, system_error) != ('', '', '', '', ''):
            return render_template('registr.html', error_1=error_1, error_2=error_2, error_3=error_3, error_4=error_4,
                                   system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3,
                                   value_4=value_4)
        pass_3 = generate_password_hash(answer_3)
        cursor.execute(
            'INSERT INTO Reg (name, password, phone, profil_img, fon_img, favourites, friends) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (answer_1, pass_3, answer_2, avatar, fon, '', ''))
        connection.commit()
        connection.close()
        session['avatar'] = avatar
        session['fon'] = fon
        session['name'] = answer_1
        with open('db2/Name.txt', 'a', encoding='utf-8') as file:
            file.write(f' {answer_1} ')
        return redirect("/personal_account")


@app.route('/personal_account', methods=['POST', 'GET'])
def personal_account():
    session.permanent = True
    name = session['name']
    index_list = []
    try:
        connection = sqlite3.connect('db2/User_2.db')
        cursor = connection.cursor()
        cursor.execute('SELECT img_url FROM Users WHERE name = ?', name)
        users = cursor.fetchall()
        connection.commit()
        connection.close()
        index_list = list(range(len(users)))
        file_list = users
    except:
        index_list = []
        file_list = []
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['avatar'] = f'/static/avatar/{filename}'
            connection = sqlite3.connect('db2/Reg_1.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE Reg SET profil_img = ? WHERE name = ?', (session['avatar'], name))
            connection.commit()
            connection.close()
            return render_template('personal_account.html', avatar=session['avatar'], name=name)
    return render_template('personal_account.html', index_list=index_list, file_list=file_list,
                           avatar=session['avatar'],
                           name=name)


@app.route('/messenger', methods=['POST', 'GET'])
def messenger():
    connection = sqlite3.connect('db2/Reg_1.db')
    cursor = connection.cursor()
    session.permanent = True
    friends_avatars = []
    count = []
    if request.method == 'GET':
        with open('db2/Name.txt', 'r', encoding='utf-8') as file:
            user = file.read().split()
        with open('db2/SMS.txt', 'r', encoding='utf-8') as f:
            user_sms = f.readlines()
            if len(user_sms) > 300:
                user_sms = user_sms[300:]
                with open('db2/SMS.txt', 'w', encoding='utf-8') as fl:
                    fl.write('\n'.join(user_sms) + '\n')
        k = 0
        for i in user:
            df = cursor.execute('SELECT profil_img FROM Reg WHERE name = ?', (i,)).fetchall()
            friends_avatars.append(df[0][0])
            count.append(k)
            k += 1
        connection.commit()
        connection.close()
        return render_template('groups.html', friends=user,
                               friends_avatars=friends_avatars, count=count, user_sms=user_sms)


@socketio.on('message')
def handleMessage(msg):
    str = f"{session['name']}: {msg}"
    with open('db2/SMS.txt', 'a', encoding='utf-8') as file:
        file.write(str + '\n')
    send(str, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=5000)
