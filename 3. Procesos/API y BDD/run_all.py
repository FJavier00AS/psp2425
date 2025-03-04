import subprocess
import time
import threading

# Función para crear la base de datos
def crear_base_datos():
    print("Creando base de datos...")
    subprocess.run(["python", "crear_db.py"])  # Ejecuta el script para crear la base de datos
    print("Base de datos creada.")

# Función para iniciar el servidor de la API Flask
def iniciar_servidor_api():
    print("Iniciando servidor de la API...")
    subprocess.run(["python", "api.py"])  # Ejecuta el script de la API
    print("Servidor de la API iniciado.")

# Función para iniciar el cliente de consola
def iniciar_cliente():
    print("Iniciando cliente para interactuar con la API...")
    subprocess.run(["python", "cliente.py"])  # Ejecuta el cliente Python que interactúa con la API
    print("Cliente finalizado.")

# Crear base de datos primero
crear_base_datos()

# Iniciar el servidor API en un hilo separado para que corra de fondo
server_thread = threading.Thread(target=iniciar_servidor_api)
server_thread.start()

# Esperar un momento para asegurar que el servidor esté listo
time.sleep(2)

# Iniciar el cliente para interactuar con la API
iniciar_cliente()

# Esperar a que el servidor termine (si es necesario detenerlo manualmente, puedes agregar lógica de cierre)
server_thread.join()