import random

# Ejercicio 1: Generación de datos
datos = [random.randint(1, 100) for _ in range(20)]

print("Lista original:")
print(datos)


# Ejercicio 3: Selection Sort (una sola función)
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


# --- Prueba con la lista generada aleatoriamente ---
lista = datos.copy()
lista_ordenada, comparaciones, intercambios = selection_sort(lista)

print("\nLista ordenada (Selection Sort):")
print(lista_ordenada)
print(f"Comparaciones: {comparaciones}")
print(f"Intercambios: {intercambios}")


# --- Recorrido manual (paso a paso) para [12, 7, 9, 3, 15] ---
print("\n--- Recorrido manual para [12, 7, 9, 3, 15] ---")
ejemplo = [12, 7, 9, 3, 15]
resultado, comp_ejemplo, interc_ejemplo = selection_sort(ejemplo, mostrar_pasos=True)

print(f"\nLista final ordenada: {resultado}")
print(f"Total de comparaciones: {comp_ejemplo}")
print(f"Total de intercambios: {interc_ejemplo}")