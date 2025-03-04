from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def conectar_db():
    return sqlite3.connect('productos.db')

# Ruta para la interfaz HTML
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para crear un producto (POST /productos)
@app.route('/productos', methods=['POST'])
def agregar_producto():
    try:
        data = request.get_json()
        nombre = data['nombre']
        precio = float(data['precio'])
        cantidad = int(data['cantidad'])
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Datos inválidos o incompletos', 'detalle': str(e)}), 400

    conn = conectar_db()
    c = conn.cursor()
    c.execute('INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)', (nombre, precio, cantidad))
    conn.commit()
    producto_id = c.lastrowid
    conn.close()
    return jsonify({'mensaje': 'Producto agregado correctamente', 'id': producto_id}), 201

# Endpoint para listar todos los productos (GET /productos)
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = conectar_db()
    c = conn.cursor()
    c.execute('SELECT * FROM productos')
    productos = c.fetchall()
    conn.close()
    
    productos_list = [
        {'id': prod[0], 'nombre': prod[1], 'precio': prod[2], 'cantidad': prod[3]}
        for prod in productos
    ]
    return jsonify(productos_list)
    #return jsonify(productos)

# Endpoint para obtener un producto específico por ID (GET /productos/<id>)
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('SELECT * FROM productos WHERE id=?', (producto_id,))
    producto = c.fetchone()
    conn.close()
    if producto:
        prod_dict = {'id': producto[0], 'nombre': producto[1], 'precio': producto[2], 'cantidad': producto[3]}
        return jsonify(prod_dict)
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

# Endpoint para actualizar un producto (PUT /productos/<id>)
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    campos = []
    valores = []

    # Permitir actualizar algunos o todos los campos
    if 'nombre' in data:
        campos.append("nombre=?")
        valores.append(data['nombre'])
    if 'precio' in data:
        try:
            valores.append(float(data['precio']))
            campos.append("precio=?")
        except ValueError:
            return jsonify({'error': 'Precio inválido'}), 400
    if 'cantidad' in data:
        try:
            valores.append(int(data['cantidad']))
            campos.append("cantidad=?")
        except ValueError:
            return jsonify({'error': 'Cantidad inválida'}), 400

    if not campos:
        return jsonify({'error': 'No se han proporcionado campos a actualizar'}), 400

    valores.append(producto_id)  # Para la condición WHERE

    query = f"UPDATE productos SET {', '.join(campos)} WHERE id=?"

    conn = conectar_db()
    c = conn.cursor()
    c.execute(query, tuple(valores))
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    conn.close()
    return jsonify({'mensaje': 'Producto actualizado correctamente'})

# Endpoint para eliminar un producto (DELETE /productos/<id>)
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('DELETE FROM productos WHERE id=?', (producto_id,))
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    conn.close()
    return jsonify({'mensaje': 'Producto eliminado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
