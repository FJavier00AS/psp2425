import threading
import multiprocessing
import time

n_hilos = 4

# funciones
def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def calcular_primos(rango):
    primos = [n for n in rango if es_primo(n)]
    #print(f"Primos en el rango {rango[0]}-{rango[-1]}: {len(primos)}")

if __name__ == "__main__":
    # sin hilos
    rango_total = range(1, 10000000)
    start = time.time()
    calcular_primos(rango_total)
    print(f"Tiempo total sin hilos: {time.time() - start} segundos")

    # con hilos
    tamaño_rango = len(rango_total) // n_hilos

    start = time.time()
    hilos = []
    for i in range(n_hilos):
        inicio = i * tamaño_rango
        fin = (i + 1) * tamaño_rango
        hilo = threading.Thread(target=calcular_primos, args=(rango_total[inicio:fin],))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(f"Tiempo total con {n_hilos} hilos: {time.time() - start} segundos")

    # con procesos
    start = time.time()
    procesos = []
    for i in range(n_hilos):
        inicio = i * tamaño_rango
        fin = (i + 1) * tamaño_rango
        proceso = multiprocessing.Process(target=calcular_primos, args=(rango_total[inicio:fin],))
        procesos.append(proceso)
        proceso.start()

    for proceso in procesos:
        proceso.join()

    print(f"Tiempo total con {n_hilos} procesos: {time.time() - start} segundos")
