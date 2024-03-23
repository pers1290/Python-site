import sqlite3

connection = sqlite3.connect('db/Reg.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Reg (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
password TEXT NOT NULL,
phone TEXT NOT NULL,
profil_img TEXT NOT NULL,
favourites TEXT NOT NULL
)
''')
# cursor.execute('INSERT INTO Users (name, topic, post_text, img_url) VALUES (?, ?, ?, ?)',
# ('Andy', 'комната', '', '/static/img/m1.jpg'))
# cursor.execute('INSERT INTO Users (name, topic, post_text, img_url) VALUES (?, ?, ?, ?)',
# ('Bill', 'комната', '', '/static/img/m2.jpg'))
# cursor.execute('INSERT INTO Users (name, topic, post_text, img_url) VALUES (?, ?, ?, ?)',
# ('Mark', 'комната', '', '/static/img/m3.jpg'))
connection.commit()
connection.close()
