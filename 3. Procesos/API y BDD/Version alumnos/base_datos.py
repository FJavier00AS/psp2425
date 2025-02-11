import sqlite3

conn = sqlite3.connect('videogames.db')

cursor = conn.cursor()

crear_tabla = '''
CREATE TABLE IF NOT EXISTS videogames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price FLOAT NOT NULL,
    genre TEXT NOT NULL,
    developer TEXT NOT NULL
);
'''

cursor.execute(crear_tabla)