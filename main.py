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
    cursor.execute('SELECT * FROM Users WHERE img_id != ""')
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
        users.append(('', 'Tinttye', 'bot', '', '', '', '', '/static/img_2/MARS-6.png'))
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
            return redirect("http://127.0.0.1:7000/tinttye")
        except:
            error = 'Ошибка'
            return render_template('change_fon.html', error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('registr.html')
    elif request.method == 'POST':
        answer_1 = request.form.get('firstname')
        answer_2 = request.form.get('surname')
        answer_3 = request.form.get('email')
        answer_4 = request.form.get('pasvord')
        connection = sqlite3.connect('db/User.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO Users (name, surname, phone, password, res1, res2, img_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (answer_1, answer_2, answer_3, answer_4, '', '', ''))
        connection.commit()
        connection.close()
        return render_template('registr.html')


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
