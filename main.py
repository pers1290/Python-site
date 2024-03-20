from flask import Flask
from flask import render_template, request
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/tinttye', methods=['POST', 'GET'])
def tinttye():
    connection = sqlite3.connect('db/User.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
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
        users.append(('', 'Tinttye', 'bot', '', '', '/static/img_2/MARS-6.png'))
    return render_template('main.html', file_list=users, index_list=index_list)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    return render_template('registration.html')


@app.route('/change_fon', methods=['POST', 'GET'])
def change_fon():
    if request.method == 'GET':
        return render_template('change_fon.html')
    elif request.method == 'POST':
        print(request.form.get('clicks'))
        return render_template('change_fon.html')


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
