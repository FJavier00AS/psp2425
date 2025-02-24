#%%
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "movimientos.db"

# Función auxiliar para conectarse a la base de datos
def conectar_db():
    return sqlite3.connect(DB_PATH)

# Añadir un movimiento
@app.route("/movimientos", methods=["POST"])
def agregar_movimiento():
    datos = request.json
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimientos (fecha, descripcion, categoria, importe)
        VALUES (?, ?, ?, ?)""", (datos.get("fecha"), datos["descripcion"], datos["categoria"], datos["importe"]))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Movimiento agregado con éxito"}), 201
#Mostrar todos los movimientos
@app.route("/movimientos", methods=["GET"])
def obtener_movimientos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movimientos")
    movimientos = cursor.fetchall()
    conn.close()
    return jsonify(movimientos)

# Mostrar movimientos del mes
@app.route("/movimientos/<int:year>/<int:month>", methods=["GET"])
def obtener_movimientos_mes(year, month):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM movimientos WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?""", (str(year), f"{month:02}"))
    movimientos = cursor.fetchall()
    conn.close()
    return jsonify(movimientos)

# Mostrar balance del mes
@app.route("/balance/<int:year>/<int:month>", methods=["GET"])
def obtener_balance_mes(year, month):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(importe) FROM movimientos WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?""", (str(year), f"{month:02}"))
    balance = cursor.fetchone()[0] or 0.0
    conn.close()
    return jsonify({"balance": balance})

# Borrar un movimiento
@app.route("/movimientos/<int:id>", methods=["DELETE"])
def borrar_movimiento(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimientos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Movimiento eliminado con éxito"})

if __name__ == "__main__":
    app.run(debug=True)

# %%
