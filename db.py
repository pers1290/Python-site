import sqlite3

connection = sqlite3.connect('db/User.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
topic TEXT NOT NULL,
post_text TEXT NOT NULL,
img_url TEXT NOT NULL
)
''')
cursor.execute('INSERT INTO Users (name, topic, post_text, img_url) VALUES (?, ?, ?, ?)',
               ('Andy', 'комната', '', '/static/img/m1.jpg'))
cursor.execute('INSERT INTO Users (name, topic, post_text, img_url) VALUES (?, ?, ?, ?)',
               ('Bill', 'комната', '', '/static/img/m2.jpg'))
cursor.execute('INSERT INTO Users (name, topic, post_text, img_url) VALUES (?, ?, ?, ?)',
               ('Mark', 'комната', '', '/static/img/m3.jpg'))
connection.commit()
connection.close()
