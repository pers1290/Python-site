from flask import Flask
from flask import render_template
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
    len_half = (len_db // 2) + 1
    if len_db % 2 == 0:
        for i in range(0, len_half, 2):
            index_list.append(i)
    else:
        for i in range(0, len_half + 1, 2):
            index_list.append(i)
        users.append(('', '', '', '', '', '/static/img_2/MARS-6.png'))
    print(users)
    print(index_list)
    return render_template('push.html', file_list=users, index_list=index_list)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
