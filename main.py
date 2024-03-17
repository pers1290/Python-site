from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/push', methods=['POST', 'GET'])
def push():
    connection = sqlite3.connect('db/User.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    return render_template('push.html', file_list=users)


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
