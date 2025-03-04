import sqlite3

def crear_db():
    # Conectar a la base de datos (se crea si no existe)
    conn = sqlite3.connect('productos.db')
    c = conn.cursor()
    
    # Crear la tabla de productos si no existe
    c.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        cantidad INTEGER NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de datos y tabla 'productos' creadas.")

if __name__ == '__main__':
    crear_db()
