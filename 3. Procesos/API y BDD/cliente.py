import requests

API_BASE_URL = 'http://127.0.0.1:5000/productos'

def agregar_producto():
    nombre = input("Nombre del producto: ")
    try:
        precio = float(input("Precio del producto: "))
        cantidad = int(input("Cantidad del producto: "))
    except ValueError:
        print("Error: El precio debe ser un número y la cantidad un entero.")
        return

    producto = {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
    response = requests.post(API_BASE_URL, json=producto)
    if response.status_code == 201:
        data = response.json()
        print(f"Producto agregado con ID {data.get('id')}.")
    else:
        print("Error al agregar el producto:", response.json())

def listar_productos():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        productos = response.json()
        if not productos:
            print("No hay productos registrados.")
        else:
            for prod in productos:
                print(f"ID: {prod['id']} | Nombre: {prod['nombre']} | Precio: {prod['precio']} | Cantidad: {prod['cantidad']}")
    else:
        print("Error al obtener los productos.")

def ver_producto():
    try:
        prod_id = int(input("Ingrese el ID del producto: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    response = requests.get(f"{API_BASE_URL}/{prod_id}")
    if response.status_code == 200:
        prod = response.json()
        print(f"ID: {prod['id']} | Nombre: {prod['nombre']} | Precio: {prod['precio']} | Cantidad: {prod['cantidad']}")
    else:
        print("Producto no encontrado o error en la solicitud.")

def actualizar_producto():
    try:
        prod_id = int(input("Ingrese el ID del producto a actualizar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    print("Ingrese los nuevos datos (deje en blanco si no desea actualizar ese campo):")
    nombre = input("Nuevo nombre: ")
    precio = input("Nuevo precio: ")
    cantidad = input("Nueva cantidad: ")

    data = {}
    if nombre:
        data['nombre'] = nombre
    if precio:
        try:
            data['precio'] = float(precio)
        except ValueError:
            print("Precio inválido.")
            return
    if cantidad:
        try:
            data['cantidad'] = int(cantidad)
        except ValueError:
            print("Cantidad inválida.")
            return

    if not data:
        print("No se proporcionaron datos para actualizar.")
        return

    response = requests.put(f"{API_BASE_URL}/{prod_id}", json=data)
    if response.status_code == 200:
        print("Producto actualizado correctamente.")
    else:
        print("Error al actualizar el producto:", response.json())

def eliminar_producto():
    try:
        prod_id = int(input("Ingrese el ID del producto a eliminar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    response = requests.delete(f"{API_BASE_URL}/{prod_id}")
    if response.status_code == 200:
        print("Producto eliminado correctamente.")
    else:
        print("Error al eliminar el producto:", response.json())

def menu():
    while True:
        print("\n--- Menú de Productos ---")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Ver producto por ID")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            listar_productos()
        elif opcion == '3':
            ver_producto()
        elif opcion == '4':
            actualizar_producto()
        elif opcion == '5':
            eliminar_producto()
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == '__main__':
    menu()
