from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['PUT'])
def add_juego(nombre, precio, genero, developer):
    conn = sqlite3.connect('videogames.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO videogames (name, price, genre, developer) VALUES (?, ?, ?, ?)", (nombre, precio, genero, developer))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def get_juegos():
    conn = sqlite3.connect('videogames.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videogames")
    juegos = cursor.fetchall()
    conn.close()
    return jsonify(juegos)

if __name__ == '__main__':
    app.run(debug=True)