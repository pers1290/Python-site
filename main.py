import os
from flask import Flask, request, redirect, render_template, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send
import sqlite3
from PIL import Image, ImageFilter, ImageEnhance
import PIL.ImageOps
from dotenv import load_dotenv
from mail import send_mail
import random
import time
from flask_sqlalchemy import SQLAlchemy

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


def contr(im, co):
    im = ImageEnhance.Sharpness(im)
    im = im.enhance(int(co) / 5)
    return im


def sat(im, sa):  # функция, изменяющая насыщенность
    im = ImageEnhance.Color(im)
    im = im.enhance(int(sa) / 10)
    return im


def bright(im, br):  # функция, изменяющая яркость
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            r, g, b = r + br, g + br, b + br
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255
            pixels[i, j] = r, g, b
    return im


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
    error_3 = ''
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
            cursor.execute('SELECT name, password, email, profil_img, fon_img FROM Reg WHERE name = ?', (answer_1,))
            users = cursor.fetchall()
            user = users[0]
            if user[2] != answer_2:
                error_3 = 'Неверный адрес электонной почты'
            if check_password_hash(user[1], answer_3) is False:
                error_2 = 'Неверный пароль'
            if (error_3, error_2, error_1) != ('', '', ''):
                return render_template('registration.html', error_1=error_1, error_2=error_2,
                                       system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3,
                                       error_3=error_3)
            session.permanent = True
            session['avatar'] = user[3]
            session['fon'] = user[4]
            connection.commit()
            connection.close()
            session['name'] = answer_1
            session['email'] = answer_2
            return redirect("/sms_cod")
        except:
            system_error = 'Вас нет в системе, зарегистрируйтесь'
            return render_template('registration.html', error_1=error_1, error_2=error_2,
                                   system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3,
                                   error_3=error_3)


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
    avatar = '/static/img_2/profil.png'
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
            'INSERT INTO Reg (name, password, email, profil_img, fon_img, favourites) VALUES (?, ?, ?, ?, ?, ?)',
            (answer_1, pass_3, answer_2, avatar, fon, ''))
        connection.commit()
        connection.close()
        session['avatar'] = avatar
        session['fon'] = fon
        session['name'] = answer_1
        session['email'] = answer_2
        with open('db2/Name.txt', 'a', encoding='utf-8') as file:
            file.write(f' {answer_1} ')
        return redirect("/sms_cod")


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


@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join('static/img', 'red.png'))
            im = Image.open('static/img/red.png')
            x, y = im.size
            if x > 500 or y > 500:
                if x / 500 > y / 500:
                    im = im.resize((500, int(y / int((x / 500)))))
                else:
                    im = im.resize((int(x / int((y / 500))), 500))
            x, y = im.size
            pixels = im.load()
            new_im = Image.new("RGB", (x, y), (0, 0, 0))
            pixels_new = new_im.load()
            for i in range(x):
                for j in range(y):
                    if type(pixels[i, j]) is tuple:
                        r, g, b = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]
                    else:
                        r, g, b = pixels[i, j], pixels[i, j], pixels[i, j]
                    pixels_new[i, j] = (r, g, b)
            new_im.save('static/img/red_.png')
            new_im.save('static/img/red.png')
            return redirect("/red")
    return render_template('post.html')


@app.route('/red', methods=['POST', 'GET'])
def red():
    co = 0
    sa = 10
    br = 0
    if request.method == 'POST':
        co = int(request.form.get('val2'))
        sa = int(request.form.get('val3'))
        br = int(request.form.get('val1'))
        im = Image.open('static/img/red.png')
        im = bright(im, br)
        im = sat(im, sa)
        im = contr(im, co)
        im.save('static/img/red_.png')
    return render_template('red.html', vall1=str(br), vall2=str(co), vall3=str(sa))


@app.route('/sms_cod', methods=['POST', 'GET'])
def sms_cod():
    if request.method == 'GET':
        cod = random.randint(10000, 100000)
        session['cod'] = str(cod)
        email = session['email']
        if send_mail(email, 'Код подтверждения', f'Ваш код: {cod}'):
            return render_template('sms_cod.html', error='')
        else:
            return render_template('sms_cod.html', error='Проблема при отправки sms')
    elif request.method == 'POST':
        cod_1 = request.form.get('cod_1')
        cod_2 = request.form.get('cod_2')
        cod_3 = request.form.get('cod_3')
        cod_4 = request.form.get('cod_4')
        cod_5 = request.form.get('cod_5')
        cod = f'{cod_1}{cod_2}{cod_3}{cod_4}{cod_5}'
        if cod == session['cod']:
            session.pop('cod')
            return redirect("/personal_account")
        else:
            return render_template('sms_cod.html', error='Неправильный код')


@socketio.on('message')
def handleMessage(msg):
    str = f"{session['name']}: {msg}"
    with open('db2/SMS.txt', 'a', encoding='utf-8') as file:
        file.write(str + '\n')
    send(str, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=8080)
