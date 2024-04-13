import sqlite3

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Reg (
# id INTEGER PRIMARY KEY,
# name TEXT NOT NULL,
# password TEXT NOT NULL,
# phone TEXT NOT NULL,
# profil_img TEXT NOT NULL,
# fon_img TEXT NOT NULL,
# favourites TEXT NOT NULL
# )
# ''')
connection = sqlite3.connect('db2/Reg.db')
cursor = connection.cursor()
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Reg (
# id INTEGER PRIMARY KEY,
# name TEXT NOT NULL,
# friends TEXT NOT NULL,
# messages TEXT NOT NULL,
# )
# ''')
# cursor.execute('UPDATE Reg SET friends = ? WHERE name = ?', ('Хомяк С Ы Рн ', 'Василий'))
# cursor.execute('UPDATE Reg SET messages = ? WHERE name = ?', ('[]', 'Хомяк'))
# cursor.execute('INSERT INTO Reg (name, friends, messages) VALUES (?, ?, ?)',
#                ('Василий', 'Хомяк', '[]'))
# cursor.execute('INSERT INTO Reg (name, friends, messages) VALUES (?, ?, ?)',
#                ('Хомяк', 'Василий', '[]'))
# cursor.execute('INSERT INTO Users (name, topic, post_text, img_url) VALUES (?, ?, ?, ?)',
# ('Mark', 'комната', '', '/static/img/m3.jpg'))
# cursor.execute(
#     'INSERT INTO Reg (name, password, phone, profil_img, fon_img, favourites) VALUES (?, ?, ?, ?, ?, ?)',
#     ('Василий', '123', answer_2, session['avatar'], session['fon'], ''))
connection.commit()
connection.close()
