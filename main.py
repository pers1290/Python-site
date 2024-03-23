from flask import Flask
from flask import render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
fon = '/static/fon_img/fon_1.jpg'


@app.route('/tinttye', methods=['POST', 'GET'])
def tinttye():
    global fon
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
    return render_template('main.html', file_list=users, index_list=index_list, fon=fon)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    return render_template('registration.html')


@app.route('/change_fon', methods=['POST', 'GET'])
def change_fon():
    global fon
    error = ''
    if request.method == 'GET':
        return render_template('change_fon.html', error=error)
    elif request.method == 'POST':
        try:
            number = int(request.form.get('text'))
            if number == 1:
                fon = '/static/fon_img/fon_1.jpg'
            elif number == 2:
                fon = '/static/fon_img/fon_2.jpg'
            elif number == 3:
                fon = '/static/fon_img/fon_3.jpg'
            return redirect("http://127.0.0.1:8000/tinttye")
        except:
            error = 'Ошибка'
            return render_template('change_fon.html', error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('registr.html')
    elif request.method == 'POST':
        answer_1 = request.form.get('firstname')
        answer_2 = request.form.get('email')
        answer_3 = request.form.get('pasvord')
        avatar = 'static/img_2/profil.png'
        try:
            # connection = sqlite3.connect('db/Reg.db')
            # cursor = connection.cursor()
            # cursor.execute('INSERT INTO Reg (name, password, phone, favourites) VALUES (?, ?, ?, ?)',
            #                (answer_1, answer_3, answer_2, avatar,''))
            # connection.commit()
            # connection.close()
            avatar = 'static/img_2/profil.png'
            name = f'   {answer_1}'
            return render_template('personal_account.html', avatar=avatar, name=name)
        except:
            return '<h1>Ошибка</h1>'


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
