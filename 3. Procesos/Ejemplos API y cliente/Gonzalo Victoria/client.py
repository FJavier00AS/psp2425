import requests
import sqlite3
from flask import jsonify

"""
Este script es un cliente que interactúa con el servidor de la aplicación
de finanzas personales. El cliente permite añadir movimientos, eliminar
movimientos, obtener los movimientos de un mes y obtener el balance de un mes.
"""

opcion = 0
while (opcion != 5):

    print("Menu de opciones")
    print("1. Añadir movimiento")
    print("2. Eliminar movimiento")
    print("3. Obtener movimientos de un mes")
    print("4. Obtener balance de un mes")
    print("5. Salir")
    try:
        # Solicitamos al usuario que introduzca una opción
        opcion = int(input("Seleccione una opción: "))
    except ValueError:
        # Si el usuario introduce un valor no numérico, mostramos un mensaje
        print("Por favor, introduzca un número válido.")
        continue

    if opcion == 1:
        # Solicitamos al usuario que introduzca los datos del movimiento
        fecha = input("Introduce la fecha del movimiento (YYYY-MM-DD): ")
        descripcion = input("Introduce la descripción del movimiento: ")
        categoria = input(
            "Introduce la categoría del movimiento "
            "(ingreso recurrente, ingreso extraordinario, "
            "gasto fijo, gasto libre, gasto extraordinario): "
        )
        try:
            importe = float(input("Introduce el importe del movimiento: "))
        except ValueError:
            print("Por favor, introduzca un importe válido.")
            continue
        # Creamos un diccionario con los datos del movimiento
        movimiento = {
            "fecha": fecha,
            "descripcion": descripcion,
            "categoria": categoria,
            "importe": importe
        }
        # Enviamos la petición POST al servidor
        response = requests.post('http://localhost:5005/add', json=movimiento)
        # Mostramos la respuesta del servidor
        print(response.json())

    elif opcion == 2:
        # Solicitamos al usuario que introduzca el id del movimiento a eliminar
        try:
            id = int(input("Introduce el id del movimiento a eliminar: "))
        except ValueError:
            print("Por favor, introduzca un id válido.")
            continue
        # Enviamos la petición DELETE al servidor
        response = requests.delete(
            'http://localhost:5005/delete', json={"id": id})
        # Mostramos la respuesta del servidor
        print(response.json())

    elif opcion == 3:
        # Solicitamos al usuario que introduzca el año y el mes
        year = input("Introduce el año del mes: ")
        month = input("Introduce el mes (1-12): ")
        # Enviamos la petición GET al servidor
        response = requests.get(
            'http://localhost:5005/movimientos_mes',
            params={"year": year, "month": month}
        )
        # Mostramos la respuesta del servidor
        print(response.json())

    elif opcion == 4:
        # Solicitamos al usuario que introduzca el año y el mes
        year = input("Introduce el año del mes: ")
        month = input("Introduce el mes (1-12): ")
        # Enviamos la petición GET al servidor
        response = requests.get(
            'http://localhost:5005/balance_mes',
            params={"year": year, "month": month}
        )
        # Mostramos la respuesta del servidor
        print(response.json())
    # Si el usuario introduce la opción 5, salimos del bucle
    elif opcion == 5:
        print("Saliendo...")
    else:
        # Si el usuario introduce una opción no válida, mostramos un mensaje
        print("Opción no válida")
