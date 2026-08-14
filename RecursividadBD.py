# ============================================================

# Ejemplos incluidos:
# 1. Máximo Común Divisor (Algoritmo de Euclides)
# 2. Conversión de Decimal a Binario
# 3. Suma Recursiva de una Lista
# 4. Búsqueda Recursiva en una Lista
# ============================================================

# ============================================================
# EJEMPLO 1: MÁXIMO COMÚN DIVISOR (MCD)
# ============================================================

def mcd(a, b):
    """
    Calcula el Máximo Común Divisor utilizando
    el algoritmo recursivo de Euclides.
    """

    if b == 0:
        return a

    return mcd(b, a % b)


# ============================================================
# EJEMPLO 2: CONVERSIÓN DE DECIMAL A BINARIO
# ============================================================

def decimal_binario(numero):
    """
    Convierte un número decimal a binario
    utilizando recursividad.
    """

    if numero == 0:
        return ""

    return decimal_binario(numero // 2) + str(numero % 2)


# ============================================================
# EJEMPLO 3: SUMA RECURSIVA DE UNA LISTA
# ============================================================

def suma_lista(lista):
    """
    Suma todos los elementos de una lista
    utilizando recursividad.
    """

    if len(lista) == 0:
        return 0

    return lista[0] + suma_lista(lista[1:])


# ============================================================
# EJEMPLO 4: BÚSQUEDA RECURSIVA EN UNA LISTA
# ============================================================

def buscar(lista, elemento, indice=0):
    """
    Busca un elemento dentro de una lista
    utilizando recursividad.
    """

    if indice >= len(lista):
        return False

    if lista[indice] == elemento:
        return True

    return buscar(lista, elemento, indice + 1)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print("        EJEMPLOS DE RECURSIVIDAD EN PYTHON")
    print("=" * 60)

    # --------------------------------------------------------
    # Ejemplo 1
    # --------------------------------------------------------

    print("\n1. MÁXIMO COMÚN DIVISOR")
    print("-" * 40)

    numero1 = 48
    numero2 = 18

    print(f"Número 1: {numero1}")
    print(f"Número 2: {numero2}")
    print(f"MCD = {mcd(numero1, numero2)}")

    # --------------------------------------------------------
    # Ejemplo 2
    # --------------------------------------------------------

    print("\n2. CONVERSIÓN DE DECIMAL A BINARIO")
    print("-" * 40)

    numero = 25

    print(f"Decimal : {numero}")
    print(f"Binario : {decimal_binario(numero)}")

    # --------------------------------------------------------
    # Ejemplo 3
    # --------------------------------------------------------

    print("\n3. SUMA RECURSIVA DE UNA LISTA")
    print("-" * 40)

    numeros = [4, 8, 10, 12]

    print("Lista:", numeros)
    print("Suma :", suma_lista(numeros))

    # --------------------------------------------------------
    # Ejemplo 4
    # --------------------------------------------------------

    print("\n4. BÚSQUEDA RECURSIVA")
    print("-" * 40)

    datos = [15, 20, 30, 45, 50]

    print("Lista:", datos)

    elemento = 45

    if buscar(datos, elemento):
        print(f"El elemento {elemento} fue encontrado.")
    else:
        print(f"El elemento {elemento} NO fue encontrado.")

    elemento = 100

    if buscar(datos, elemento):
        print(f"El elemento {elemento} fue encontrado.")
    else:
        print(f"El elemento {elemento} NO fue encontrado.")

    print("\n" + "=" * 60)
    print("Fin del programa")
    print("=" * 60)


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()