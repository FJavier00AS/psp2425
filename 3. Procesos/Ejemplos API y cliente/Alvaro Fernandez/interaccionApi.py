import requests

BASE_URL = "http://127.0.0.1:5000"

def agregar_movimiento():
    descripcion = input("Descripción: ")
    categoria = input("Categoría (ingreso recurrente, ingreso extraordinario, gasto fijo, gasto libre, gasto extraordinario): ")
    importe = float(input("Importe: "))
    fecha = input("Fecha (YYYY-MM-DD, opcional): ") or None
    
    # Si la categoría es un gasto, el importe debe ser negativo
    if "gasto" in categoria.lower():
        importe = -abs(importe)
    
    datos = {"descripcion": descripcion, "categoria": categoria, "importe": importe, "fecha": fecha}
    respuesta = requests.post(f"{BASE_URL}/movimientos", json=datos)
    print(respuesta.json()["mensaje"])

def mostrar_movimientos_mes():
    year = input("Año (YYYY): ")
    month = input("Mes (MM): ")
    respuesta = requests.get(f"{BASE_URL}/movimientos/{year}/{month}")
    movimientos = respuesta.json()
    for mov in movimientos:
        print(mov)

def mostrar_balance_mes():
    year = input("Año (YYYY): ")
    month = input("Mes (MM): ")
    respuesta = requests.get(f"{BASE_URL}/movimientos/{year}/{month}")
    movimientos = respuesta.json()
    
    balance = sum(mov[4] for mov in movimientos)  # Sumar todos los importes considerando gastos negativos
    print(f"Balance: {balance}")

def borrar_movimiento():
    id_mov = input("ID del movimiento a borrar: ")
    respuesta = requests.delete(f"{BASE_URL}/movimientos/{id_mov}")
    print(respuesta.json()["mensaje"])

def main():
    while True:
        print("\nOpciones:")
        print("1. Añadir movimiento")
        print("2. Mostrar movimientos del mes")
        print("3. Mostrar balance del mes")
        print("4. Borrar un movimiento")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            agregar_movimiento()
        elif opcion == "2":
            mostrar_movimientos_mes()
        elif opcion == "3":
            mostrar_balance_mes()
        elif opcion == "4":
            borrar_movimiento()
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()