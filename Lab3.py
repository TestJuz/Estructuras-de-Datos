import random
import time


datos = [random.randint(1, 100) for _ in range(20)]
datos100 = [random.randint(1, 100) for _ in range(100)]
datos500 = [random.randint(1, 500) for _ in range(500)]
datos1000 = [random.randint(1, 1000) for _ in range(1000)]
datos5000 = [random.randint(1, 5000) for _ in range(5000)]
datos100000 = [random.randint(1, 100000) for _ in range(100000)]

print("Lista original:")
print(datos)



def selection_sort(lista, mostrar_pasos=False):
    comparaciones = 0
    intercambios = 0
    n = len(lista)

    if mostrar_pasos:
        print(f"Estado inicial: {lista}")

    for i in range(n - 1):
        indice_menor = i
        for j in range(i + 1, n):
            comparaciones += 1
            if lista[j] < lista[indice_menor]:
                indice_menor = j

        if indice_menor != i:
            lista[i], lista[indice_menor] = lista[indice_menor], lista[i]
            intercambios += 1
            if mostrar_pasos:
                print(f"Iteración {i + 1}: se intercambió posición {i} con posición {indice_menor} -> {lista}")
        else:
            if mostrar_pasos:
                print(f"Iteración {i + 1}: no hubo intercambio (el menor ya estaba en su lugar) -> {lista}")

    return lista, comparaciones, intercambios



lista = datos.copy()
lista_ordenada, comparaciones, intercambios = selection_sort(lista)

print("\nLista ordenada (Selection Sort):")
print(lista_ordenada)
print(f"Comparaciones: {comparaciones}")
print(f"Intercambios: {intercambios}")



print("\n--- Recorrido manual para [12, 7, 9, 3, 15] ---")
ejemplo = [12, 7, 9, 3, 15]
resultado, comp_ejemplo, interc_ejemplo = selection_sort(ejemplo, mostrar_pasos=True)

print(f"\nLista final ordenada: {resultado}")
print(f"Total de comparaciones: {comp_ejemplo}")
print(f"Total de intercambios: {interc_ejemplo}")


#-----------------Times-----------------
print("\nTiempos de carga: \n")

lista100 = datos100.copy()
lista500 = datos500.copy()
lista1000 = datos1000.copy()
lista5000 = datos5000.copy()

print("Ordenar 100")
inicio = time.perf_counter()
lista_ordenada100, comparaciones, intercambios = selection_sort(lista100)
fin = time.perf_counter()
print("Tiempo: " + str( fin - inicio)+"\n")

print("Ordenar 500")
inicio = time.perf_counter()
lista_ordenada500, comparaciones, intercambios = selection_sort(lista500)
fin = time.perf_counter()
print("Tiempo: " + str( fin - inicio)+"\n")

print("Ordenar 1000")
inicio = time.perf_counter()
lista_ordenada1000, comparaciones, intercambios = selection_sort(lista1000)
fin = time.perf_counter()
print("Tiempo: " + str( fin - inicio)+"\n")

print("Ordenar 5000")
inicio = time.perf_counter()
lista_ordenada5000, comparaciones, intercambios = selection_sort(lista5000)
fin = time.perf_counter()
print("Tiempo: " + str( fin - inicio)+"\n")

#--------Condiciones de entrada--------

print("\n Condiciones de entrada")

ListaAleatoria = random.sample(range(1, 10000), 1000)
ListaOrdenada = list(range(1000))
ListaInversamente = list(range(1000, 0, -1))

inicio = time.perf_counter()
resultado1, comp_ejemplo1, interc_ejemplo1 = selection_sort(ListaAleatoria)
fin = time.perf_counter()
print(f"Total de comparaciones: {comp_ejemplo1}")
print(f"Total de intercambios: {interc_ejemplo1}")
print("Tiempo: " + str( fin - inicio)+"\n")

inicio = time.perf_counter()
resultado2, comp_ejemplo2, interc_ejemplo2 = selection_sort(ListaOrdenada)
fin = time.perf_counter()
print(f"Total de comparaciones: {comp_ejemplo2}")
print(f"Total de intercambios: {interc_ejemplo2}")
print("Tiempo: " + str( fin - inicio)+"\n")

inicio = time.perf_counter()
resultado3, comp_ejemplo3, interc_ejemplo3 = selection_sort(ListaInversamente)
fin = time.perf_counter()
print(f"Total de comparaciones: {comp_ejemplo3}")
print(f"Total de intercambios: {interc_ejemplo3}")
print("Tiempo: " + str( fin - inicio)+"\n")


#--------Comparacion con python--------

print("\n Comparacion con python")

inicio = time.perf_counter()
sorted(datos100000)
fin = time.perf_counter()
print("Tiempo de sorted: " + str( fin - inicio)+"\n")

inicio = time.perf_counter()
selection_sort(datos100000.copy())
fin = time.perf_counter()
print("Tiempo de selection_sort: " + str( fin - inicio)+"\n")


