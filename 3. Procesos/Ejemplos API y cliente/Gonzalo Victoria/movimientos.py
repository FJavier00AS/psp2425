import sqlite3

"""
Este módulo proporciona funciones para gestionar los movimientos de una base de datos SQLite.
Cada movimiento tiene los siguientes campos:
- id: identificador único del movimiento (número entero)
- fecha: fecha del movimiento (cadena de texto en formato 'YYYY-MM-DD')
- descripcion: descripción del movimiento (cadena de texto)
- categoria: categoría del movimiento (cadena de texto)
- importe: importe del movimiento (número decimal)
"""


def get_movimientos():
    """Devuelve una lista con todos los movimientos de la base de datos.
    Cada movimiento es un diccionario con los campos 'id', 'fecha', 'descripcion', 'categoria' e 'importe'."""
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('movimientos.db')
        cursor = conn.cursor()
        # Obtener todos los movimientos
        cursor.execute('SELECT * FROM movimientos')
        movimientos = cursor.fetchall()
    except sqlite3.Error as e:
        # En caso de error, devolver una lista vacía
        print(f"Database error: {e}")
        movimientos = []
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
    return movimientos


def get_movimientos_mes(year, month):
    """Devuelve una lista con todos los movimientos del mes y año especificados.
    Cada movimiento es un diccionario con los campos 'id', 'fecha', 'descripcion', 'categoria' e 'importe'.
    El mes debe ser un número entre 1 y 12.
    El año debe ser un número de 4 dígitos.
    Los movimientos se devuelven ordenados por fecha.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('movimientos.db')
        cursor = conn.cursor()
        # Obtener los movimientos del mes y año especificados
        cursor.execute('''
            SELECT * FROM movimientos
            WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?
        ''', (year, month.zfill(2)))
        movimientos = cursor.fetchall()
    except sqlite3.Error as e:
        # En caso de error, devolver una lista vacía
        print(f"Database error: {e}")
        movimientos = []
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
    return movimientos


def add_movimiento(movimiento):
    """Añade un nuevo movimiento a la base de datos.
    El movimiento es un diccionario con los campos 'fecha', 'descripcion', 'categoria' e 'importe'.
    La fecha debe tener el formato 'YYYY-MM-DD'.
    La categoría debe ser una cadena de texto.
    El importe debe ser un número decimal.
    Devuelve True si el movimiento se añadió correctamente, False en caso contrario
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('movimientos.db')
        cursor = conn.cursor()
        # Insertar el nuevo movimiento en la base de datos
        cursor.execute(
            'INSERT INTO movimientos (fecha, descripcion, categoria, importe) VALUES (?, ?, ?, ?)',
            (movimiento['fecha'], movimiento['descripcion'],
             movimiento['categoria'], movimiento['importe'])
        )
        # Confirmar la transacción
        conn.commit()
        success = True
    except sqlite3.Error as e:
        # En caso de error, devolver False
        print(f"Database error: {e}")
        success = False
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
    return success


def delete_movimiento(id):
    """Elimina un movimiento de la base de datos.
    El id es el identificador del movimiento a eliminar.
    Devuelve True si el movimiento se eliminó correctamente, False en caso contrario
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('movimientos.db')
        cursor = conn.cursor()
        # Eliminar el movimiento de la base de datos
        cursor.execute('DELETE FROM movimientos WHERE id = ?', (id,))
        conn.commit()
        success = True
    except sqlite3.Error as e:
        # En caso de error, devolver False
        print(f"Database error: {e}")
        success = False
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
    return success


def get_balance_mes(year, month):
    """Devuelve el balance total de los movimientos del mes y año especificados.
    El mes debe ser un número entre 1 y 12.
    El año debe ser un número de 4 dígitos.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('movimientos.db')
        cursor = conn.cursor()
        # Obtener el balance total de los movimientos del mes y año especificados
        cursor.execute('''
            SELECT SUM(importe) FROM movimientos
            WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?
        ''', (year, month.zfill(2)))
        # Obtener el balance total
        balance = cursor.fetchone()[0]
    except sqlite3.Error as e:
        # En caso de error, devolver 0
        print(f"Database error: {e}")
        balance = 0
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
    return balance if balance is not None else 0
