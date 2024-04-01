import os
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
UPLOAD_FOLDER = 'static/avatar/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FON_LIST = {'1': '/static/fon_img/fon_1.jpg', '2': '/static/fon_img/fon_2.jpg', '3': '/static/fon_img/fon_3.jpg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
fon = '/static/fon_img/fon_1.jpg'
avatar = 'static/img_2/profil.png'
name = ''


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/tinttye', methods=['POST', 'GET'])
def tinttye():
    global fon
    global avatar
    global name
    connection = sqlite3.connect('db/User.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    len_db = len(users)
    index_list = []
    if len_db % 2 == 0:
        for i in range(0, len_db, 2):
            index_list.append(i)
    else:
        for i in range(0, len_db + 1, 2):
            index_list.append(i)
        users.append(('', 'Tinttye bot', '', '', '/static/img_2/MARS-6.png'))
    return render_template('main.html', file_list=users, index_list=index_list, fon=fon, avatar=avatar, name=name)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    global name
    global avatar
    global fon
    error_1 = ''
    error_2 = ''
    value_1, value_2, value_3 = '', '', ''
    system_error = ''
    if request.method == 'GET':
        if name == '':
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
        connection = sqlite3.connect('db/Reg.db')
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT name, password, phone, profil_img, fon_img FROM Reg WHERE name = ?', (answer_1,))
            users = cursor.fetchall()
            user = users[0]
            if user[1] != answer_3:
                error_2 = 'Неверный пароль'
                return render_template('registration.html', error_1=error_1, error_2=error_2,
                                       system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3)
            avatar = user[3]
            fon = user[4]
            connection.commit()
            connection.close()
            name = answer_1
            return redirect("/personal_account")
        except:
            system_error = 'Вас не в системе, зарегистрируйтесь'
            return render_template('registration.html', error_1=error_1, error_2=error_2,
                                   system_error=system_error, value_1=value_1, value_2=value_2, value_3=value_3)


@app.route('/change_fon', methods=['POST', 'GET'])
def change_fon():
    global fon
    global FON_LIST
    global name
    error = ''
    if request.method == 'GET':
        return render_template('change_fon.html', error=error)
    elif request.method == 'POST':
        number = request.form.get('email')
        if number not in ('1', '2', '3'):
            error = 'Может быть 1, 2 или 3'
            return render_template('change_fon.html', error=error)
        number = request.form.get('email')
        fon = FON_LIST[number]
        if name != '':
            connection = sqlite3.connect('db/Reg.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE Reg SET fon_img = ? WHERE name = ?', (fon, name))
            connection.commit()
            connection.close()
        return redirect("/tinttye")


@app.route('/login', methods=['POST', 'GET'])
def login():
    global name
    global avatar
    global fon
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
        connection = sqlite3.connect('db/Reg.db')
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
        cursor.execute(
            'INSERT INTO Reg (name, password, phone, profil_img, fon_img, favourites) VALUES (?, ?, ?, ?, ?, ?)',
            (answer_1, answer_3, answer_2, avatar, fon, ''))
        connection.commit()
        connection.close()
        name = answer_1
        return redirect("/personal_account")


@app.route('/personal_account', methods=['POST', 'GET'])
def personal_account():
    global name
    global avatar
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            avatar = f'/static/avatar/{filename}'
            connection = sqlite3.connect('db/Reg.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE Reg SET profil_img = ? WHERE name = ?', (avatar, name))
            connection.commit()
            connection.close()
            return render_template('personal_account.html', avatar=avatar, name=name)
    return render_template('personal_account.html', avatar=avatar, name=name)


@app.route('/messenger', methods=['POST', 'GET'])
def messenger():
    if request.method == 'GET':
        return render_template('messenger.html')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
