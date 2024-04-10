import os
from flask import Flask, request, redirect, render_template, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send
import sqlite3
import json
import asyncio

app = Flask(__name__)
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
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    len_db = len(users)
    index_list = []
    session.permanent = True
    if 'name' in session:
        name = session['name']
    if 'fon' in session:
        fon = session['fon']
    if 'avatar' in session:
        avatar = session['avatar']
    if len_db % 2 == 0:
        for i in range(0, len_db, 2):
            index_list.append(i)
    else:
        for i in range(0, len_db + 1, 2):
            index_list.append(i)
        users.append(('', 'Tinttye bot', '', '/static/img_2/MARS-6.png', ''))
    return render_template('main.html', file_list=users, index_list=index_list, fon=fon, avatar=avatar, name=name,
                           error=error)


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
        connection = sqlite3.connect('db2/Reg.db')
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
        connection = sqlite3.connect('db2/Reg.db')
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
        connection = sqlite3.connect('db2/Reg.db')
        cursor = connection.cursor()
        if answer_4 != answer_3:
            error_2 = 'Пароли не совпадают'
            error_3 = 'Пароли не совпадают'
        cursor.execute('SELECT name FROM Reg')
        name_user = cursor.fetchall()
        if len(name_user) > 0 and answer_1 in name_user[0]:
            cursor.execute('SELECT password FROM Reg WHERE name = ?', (answer_1,))
            name_user = cursor.fetchall()
            if name_user[0][0] == answer_3:
                system_error = 'Вы уже зарегистрированы в системе'
            else:
                error_1 = 'Такой никнейм есть, придумайте новый'
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
        return redirect("/personal_account")


@app.route('/personal_account', methods=['POST', 'GET'])
def personal_account():
    session.permanent = True
    name = session['name']
    connection = sqlite3.connect('db2/User_2.db')
    cursor = connection.cursor()
    cursor.execute('SELECT img_url FROM Users WHERE name = ?', name)
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    index_list = list(range(len(users)))
    print(index_list)
    print(name)
    print(users)
    print(users[0])
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
            connection = sqlite3.connect('db2/Reg.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE Reg SET profil_img = ? WHERE name = ?', (session['avatar'], name))
            connection.commit()
            connection.close()
            return render_template('personal_account.html', avatar=session['avatar'], name=name)
    return render_template('personal_account.html', file_list=users, index_list=index_list, avatar=session['avatar'],
                           name=name)


@app.route('/messenger', methods=['POST', 'GET'])
def messenger():
    connection = sqlite3.connect('db2/Reg.db')
    cursor = connection.cursor()
    session.permanent = True
    name = session['name']
    error = ''
    if 'error2' in session:
        error = session['error2']
        session.pop('error2')
    friends = []
    friends_avatars = []
    count = []
    if request.method == 'GET':
        user = cursor.execute('SELECT friends FROM Reg WHERE name = ?', (name,)).fetchall()
        for h in user[0][0].split():
            friends.append(h)
        k = 0
        for i in friends:
            df = cursor.execute('SELECT profil_img FROM Reg WHERE name = ?', (i,)).fetchall()
            friends_avatars.append(df[0][0])
            count.append(k)
            k += 1
        connection.commit()
        connection.close()
        return render_template('groups.html', name=name, friends=friends,
                               friends_avatars=friends_avatars, count=count, error=error)
    elif request.method == 'POST':
        answer_1 = request.form.get('friends')
        answer_1 = answer_1.title()
        # try:
        connection2 = sqlite3.connect('db2/Messanger.db')
        cursor2 = connection2.cursor()
        sd = cursor2.execute('SELECT name FROM Reg').fetchall()
        for i in sd:
            if answer_1 in i[0]:
                session['error2'] = 'Такой чат есть'
                return redirect('/messenger')
        user_1 = cursor.execute('SELECT friends FROM Reg WHERE name = ?', (answer_1,)).fetchall()
        user_2 = cursor.execute('SELECT friends FROM Reg WHERE name = ?', (name,)).fetchall()
        user_1 = user_1[0][0] + f'{name} '
        user_2 = user_2[0][0] + f'{answer_1} '
        cursor.execute('UPDATE Reg SET friends = ? WHERE name = ?', (user_1, answer_1))
        cursor.execute('UPDATE Reg SET friends = ? WHERE name = ?', (user_2, name))
        cursor2.execute(
            'INSERT INTO Reg (name, friends, messages) VALUES (?, ?, ?)',
            (answer_1, name, '[]'))
        cursor2.execute(
            'INSERT INTO Reg (name, friends, messages) VALUES (?, ?, ?)',
            (name, answer_1, '[]'))
        connection2.commit()
        connection2.close()
        connection.commit()
        connection.close()
        session.pop('error2')
        return redirect('/messenger')
        # except:
        #     session['error2'] = 'Ник не найден'
        #     connection.commit()
        #     connection.close()
        #     return redirect('/messenger')


@app.route('/chat/<name>', methods=['POST', 'GET'])
def chat(name):
    session['friend'] = name
    connection2 = sqlite3.connect('db2/Reg.db')
    cursor2 = connection2.cursor()
    df = cursor2.execute('SELECT profil_img FROM Reg WHERE name = ?', (name,)).fetchall()
    connection2.commit()
    connection2.close()
    connection = sqlite3.connect('db2/Messanger.db')
    cursor = connection.cursor()
    user_sms = cursor.execute('SELECT messages FROM Reg WHERE name = ?', (name,)).fetchall()
    user_sms = json.loads(user_sms[0][0])
    if request.method == 'GET':
        return render_template('friend.html', name=session['name'],
                               df=df[0][0], friend=name, user_sms=user_sms)


@socketio.on('message')
def handleMessage(msg):
    session.permanent = True
    name = session['name']
    connection = sqlite3.connect('db2/Messanger.db')
    cursor = connection.cursor()
    user_1 = cursor.execute('SELECT messages FROM Reg WHERE name = ?', (name,)).fetchall()
    user_1 = user_1[0][0]
    user_1 = json.loads(user_1)
    user_1.append((name, msg))
    d = json.dumps(user_1, ensure_ascii=False)
    cursor.execute('UPDATE Reg SET messages = ? WHERE name = ?', (d, name))
    cursor.execute('UPDATE Reg SET messages = ? WHERE name = ?', (d, session['friend']))
    connection.commit()
    connection.close()

    send(msg[:20], broadcast=True)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=8000)
