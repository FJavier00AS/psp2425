from flask import Flask, jsonify, request
from movimientos import add_movimiento, get_balance_mes, get_movimientos_mes, delete_movimiento, get_movimientos

# Creación de la aplicación
app = Flask(__name__)


@app.route('/add', methods=['POST'])
def anadir_movimiento():
    """Endpoint para añadir un movimiento
    Se espera un JSON con los datos del movimiento
    si no se proporcionan los datos necesarios se devolverá un error 500
    si se añade correctamente se devolverá un código 201 Created
"""
    try:
        # Obtenemos los datos de la petición
        movimiento = {
            "fecha": request.json['fecha'],
            "descripcion": request.json['descripcion'],
            "categoria": request.json['categoria'],
            "importe": request.json['importe']
        }
        # Añadimos el movimiento a la base de datos
        add_movimiento(movimiento)
        # Devolvemos código 201 Created
        return jsonify({"mensaje": "Movimiento añadido"}), 201
    except Exception as e:
        # Manejamos errores con código 500
        return jsonify({"error": str(e)}), 500


@app.route('/delete', methods=['DELETE'])
def eliminar_movimiento():
    """Endpoint para eliminar un movimiento utilizando su id
    Se espera un JSON con el id del movimiento a eliminar
    si no se proporciona el id se devolverá un error 500
    si se elimina correctamente se devolverá un código 200 OK
    """

    try:
        # Obtenemos el id del movimiento a eliminar
        id = request.json['id']
        delete_movimiento(id)
        return jsonify({"mensaje": "Movimiento eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/movimientos_mes', methods=['GET'])
def obtener_movimientos():
    """Endpoint para obtener los movimientos de un mes
    Se espera un año y un mes como parámetros
    si no se proporcionan los parámetros se devolverá un error 500
    si se obtienen los movimientos correctamente se devolverá un código 200 OK
    """
    try:
        year = request.args.get('year')
        month = request.args.get('month')
        movimientos = get_movimientos_mes(year, month)
        return jsonify(movimientos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/balance_mes', methods=['GET'])
def obtener_balance():
    """Endpoint para obtener el balance de un mes
    Se espera un año y un mes como parámetros
    si no se proporcionan los parámetros se devolverá un error 500
    si se obtiene el balance correctamente se devolverá un código 200 OK
    """
    try:
        year = request.args.get('year')
        month = request.args.get('month')
        balance = get_balance_mes(year, month)
        return jsonify({"balance": balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def obtener():
    """Endpoint para obtener todos los movimientos
    si se obtienen los movimientos correctamente se devolverá un código 200 OK
    si no se obtienen los movimientos se devolverá un error 500
    """
    try:
        data = get_movimientos()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    """Ejecución del servidor
    Se ejecuta el servidor en el puerto 5005
    """
    app.run(debug=True, host='0.0.0.0', port=5005)
