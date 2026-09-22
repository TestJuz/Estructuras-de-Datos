"""
test_arboles.py
----------------
Pruebas unitarias (con "assert" simple, sin dependencias externas)
para validar la corrección de los 4 módulos de árboles. Cubre casos
límite importantes: árboles vacíos, un solo nodo, los 3 casos de
eliminación en BST, las 4 rotaciones del AVL, y manejo de archivos
mal formados.

Ejecutar con:  python3 test_arboles.py
Si todo pasa, no debería lanzar ningún AssertionError y termina
imprimiendo "TODAS LAS PRUEBAS PASARON".
"""

import os
import tempfile

from arbol_general import ArbolGeneral
from arbol_binario import ArbolBinario
from arbol_bst import ArbolBST
from arbol_avl import ArbolAVL

pruebas_ejecutadas = 0


def prueba(nombre):
    """Decorador simple que imprime el nombre de cada prueba al pasar."""
    def decorador(func):
        def envoltura():
            global pruebas_ejecutadas
            func()
            pruebas_ejecutadas += 1
            print(f"  ✓ {nombre}")
        return envoltura
    return decorador


def escribir_temporal(contenido: str) -> str:
    """Crea un archivo temporal con el contenido dado y devuelve su ruta."""
    fd, ruta = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


# ======================================================================
# ÁRBOL GENERAL
# ======================================================================

@prueba("Árbol general: construcción manual y preorden")
def test_general_manual():
    arbol = ArbolGeneral()
    arbol.insertar(None, "A")
    arbol.insertar("A", "B")
    arbol.insertar("A", "C")
    arbol.insertar("B", "D")
    assert arbol.preorden() == ["A", "B", "D", "C"]
    assert arbol.altura() == 2
    assert arbol.contar_nodos() == 4


@prueba("Árbol general: carga desde archivo y round-trip")
def test_general_archivo():
    contenido = "ROOT,X\nX,Y\nX,Z\nY,W\n"
    ruta = escribir_temporal(contenido)
    arbol = ArbolGeneral()
    arbol.cargar_desde_archivo(ruta)
    assert arbol.raiz.dato == "X"
    assert arbol.contar_nodos() == 4

    ruta_salida = ruta + ".out"
    arbol.guardar_en_archivo(ruta_salida)
    arbol2 = ArbolGeneral()
    arbol2.cargar_desde_archivo(ruta_salida)
    assert arbol.preorden() == arbol2.preorden()

    os.remove(ruta)
    os.remove(ruta_salida)


@prueba("Árbol general: archivo mal formado lanza ValueError")
def test_general_archivo_invalido():
    ruta = escribir_temporal("esto,no,es,valido\n")
    arbol = ArbolGeneral()
    try:
        arbol.cargar_desde_archivo(ruta)
        assert False, "Debió lanzar ValueError"
    except ValueError:
        pass
    finally:
        os.remove(ruta)


@prueba("Árbol general: archivo sin ROOT lanza ValueError")
def test_general_sin_root():
    ruta = escribir_temporal("A,B\n")
    arbol = ArbolGeneral()
    try:
        arbol.cargar_desde_archivo(ruta)
        assert False, "Debió lanzar ValueError por falta de ROOT"
    except ValueError:
        pass
    finally:
        os.remove(ruta)


# ======================================================================
# ÁRBOL BINARIO
# ======================================================================

@prueba("Árbol binario: recorridos sobre árbol conocido")
def test_binario_recorridos():
    arbol = ArbolBinario()
    ruta = escribir_temporal("8,3,10,1,6,-,14\n")
    arbol.cargar_desde_archivo(ruta)
    os.remove(ruta)

    assert arbol.preorden() == [8, 3, 1, 6, 10, 14]
    assert arbol.inorden() == [1, 3, 6, 8, 10, 14]
    assert arbol.postorden() == [1, 6, 3, 14, 10, 8]
    assert arbol.por_niveles() == [8, 3, 10, 1, 6, 14]
    assert arbol.altura() == 2


@prueba("Árbol binario: árbol vacío")
def test_binario_vacio():
    ruta = escribir_temporal("-\n")
    arbol = ArbolBinario()
    arbol.cargar_desde_archivo(ruta)
    os.remove(ruta)
    assert arbol.raiz is None
    assert arbol.preorden() == []
    assert arbol.altura() == -1


@prueba("Árbol binario: un solo nodo")
def test_binario_un_nodo():
    ruta = escribir_temporal("42\n")
    arbol = ArbolBinario()
    arbol.cargar_desde_archivo(ruta)
    os.remove(ruta)
    assert arbol.raiz.dato == 42
    assert arbol.altura() == 0


@prueba("Árbol binario: destruir() deja el árbol vacío")
def test_binario_destruir():
    arbol = ArbolBinario()
    ruta = escribir_temporal("1,2,3\n")
    arbol.cargar_desde_archivo(ruta)
    os.remove(ruta)
    arbol.destruir()
    assert arbol.raiz is None


# ======================================================================
# BST
# ======================================================================

@prueba("BST: inserción mantiene el inorden ordenado")
def test_bst_insertar():
    arbol = ArbolBST()
    for v in [8, 3, 10, 1, 6, 14, 4, 7]:
        arbol.insertar(v)
    assert arbol.inorden() == [1, 3, 4, 6, 7, 8, 10, 14]
    assert arbol.es_valido_bst()


@prueba("BST: buscar existente e inexistente")
def test_bst_buscar():
    arbol = ArbolBST()
    for v in [5, 2, 8]:
        arbol.insertar(v)
    assert arbol.buscar(2) is True
    assert arbol.buscar(99) is False


@prueba("BST: eliminar caso 1 (hoja)")
def test_bst_eliminar_hoja():
    arbol = ArbolBST()
    for v in [5, 2, 8]:
        arbol.insertar(v)
    arbol.eliminar(2)
    assert arbol.inorden() == [5, 8]
    assert arbol.es_valido_bst()


@prueba("BST: eliminar caso 2 (un hijo)")
def test_bst_eliminar_un_hijo():
    arbol = ArbolBST()
    for v in [5, 2, 8, 1]:  # 2 tiene un solo hijo (1)
        arbol.insertar(v)
    arbol.eliminar(2)
    assert arbol.inorden() == [1, 5, 8]
    assert arbol.es_valido_bst()


@prueba("BST: eliminar caso 3 (dos hijos)")
def test_bst_eliminar_dos_hijos():
    arbol = ArbolBST()
    for v in [8, 3, 10, 1, 6, 14, 4, 7]:
        arbol.insertar(v)
    arbol.eliminar(3)  # 3 tiene dos hijos: 1 y 6
    assert arbol.inorden() == [1, 4, 6, 7, 8, 10, 14]
    assert arbol.es_valido_bst()


@prueba("BST: eliminar la raíz completa")
def test_bst_eliminar_raiz():
    arbol = ArbolBST()
    for v in [8, 3, 10]:
        arbol.insertar(v)
    arbol.eliminar(8)
    assert arbol.inorden() == [3, 10]
    assert arbol.es_valido_bst()


@prueba("BST: eliminar un valor inexistente no rompe el árbol")
def test_bst_eliminar_inexistente():
    arbol = ArbolBST()
    for v in [8, 3, 10]:
        arbol.insertar(v)
    arbol.eliminar(999)
    assert arbol.inorden() == [3, 8, 10]


@prueba("BST: round-trip preserva la forma exacta (no solo los valores)")
def test_bst_round_trip_forma():
    arbol = ArbolBST()
    for v in [8, 3, 10, 1, 6, 14, 4, 7]:
        arbol.insertar(v)

    ruta = tempfile.mktemp(suffix=".txt")
    arbol.guardar_en_archivo(ruta)

    arbol2 = ArbolBST()
    arbol2.cargar_forma_exacta_desde_archivo(ruta)
    os.remove(ruta)

    # La forma exacta se preserva: incluso el preorden debe coincidir
    def preorden(a):
        r = []
        def rec(n):
            if n is None:
                return
            r.append(n.dato)
            rec(n.izquierdo)
            rec(n.derecho)
        rec(a.raiz)
        return r

    assert preorden(arbol) == preorden(arbol2)


# ======================================================================
# AVL
# ======================================================================

@prueba("AVL: rotación simple derecha (caso Izquierda-Izquierda)")
def test_avl_rotacion_ll():
    arbol = ArbolAVL()
    for v in [30, 20, 10]:  # fuerza LL
        arbol.insertar(v)
    assert arbol.raiz.dato == 20
    assert arbol.raiz.izquierdo.dato == 10
    assert arbol.raiz.derecho.dato == 30
    assert arbol.esta_balanceado()


@prueba("AVL: rotación simple izquierda (caso Derecha-Derecha)")
def test_avl_rotacion_rr():
    arbol = ArbolAVL()
    for v in [10, 20, 30]:  # fuerza RR
        arbol.insertar(v)
    assert arbol.raiz.dato == 20
    assert arbol.raiz.izquierdo.dato == 10
    assert arbol.raiz.derecho.dato == 30
    assert arbol.esta_balanceado()


@prueba("AVL: rotación doble Izquierda-Derecha")
def test_avl_rotacion_ld():
    arbol = ArbolAVL()
    for v in [30, 10, 20]:  # fuerza LR
        arbol.insertar(v)
    assert arbol.raiz.dato == 20
    assert arbol.raiz.izquierdo.dato == 10
    assert arbol.raiz.derecho.dato == 30
    assert arbol.esta_balanceado()


@prueba("AVL: rotación doble Derecha-Izquierda")
def test_avl_rotacion_di():
    arbol = ArbolAVL()
    for v in [10, 30, 20]:  # fuerza RL
        arbol.insertar(v)
    assert arbol.raiz.dato == 20
    assert arbol.raiz.izquierdo.dato == 10
    assert arbol.raiz.derecho.dato == 30
    assert arbol.esta_balanceado()


@prueba("AVL: inserción en orden ascendente permanece balanceado")
def test_avl_orden_ascendente():
    arbol = ArbolAVL()
    for v in range(1, 101):  # 1..100 en orden -> degeneraría un BST normal
        arbol.insertar(v)
    assert arbol.esta_balanceado()
    # Con 100 nodos balanceados, la altura debe ser cercana a log2(100)≈6.6
    assert arbol.altura() <= 8, f"Altura inesperadamente alta: {arbol.altura()}"
    assert arbol.inorden() == list(range(1, 101))


@prueba("AVL: round-trip preserva la forma y el balance")
def test_avl_round_trip():
    arbol = ArbolAVL()
    for v in [10, 20, 30, 40, 50, 25, 5, 1]:
        arbol.insertar(v)

    ruta = tempfile.mktemp(suffix=".txt")
    arbol.guardar_en_archivo(ruta)

    arbol2 = ArbolAVL()
    arbol2.cargar_forma_exacta_desde_archivo(ruta)
    os.remove(ruta)

    assert arbol.inorden() == arbol2.inorden()
    assert arbol2.esta_balanceado()
    assert arbol.altura() == arbol2.altura()


def main():
    print("Ejecutando pruebas unitarias...\n")

    todas_las_pruebas = [
        test_general_manual, test_general_archivo,
        test_general_archivo_invalido, test_general_sin_root,
        test_binario_recorridos, test_binario_vacio,
        test_binario_un_nodo, test_binario_destruir,
        test_bst_insertar, test_bst_buscar, test_bst_eliminar_hoja,
        test_bst_eliminar_un_hijo, test_bst_eliminar_dos_hijos,
        test_bst_eliminar_raiz, test_bst_eliminar_inexistente,
        test_bst_round_trip_forma,
        test_avl_rotacion_ll, test_avl_rotacion_rr,
        test_avl_rotacion_ld, test_avl_rotacion_di,
        test_avl_orden_ascendente, test_avl_round_trip,
    ]

    for test in todas_las_pruebas:
        test()

    print(f"\n{pruebas_ejecutadas}/{len(todas_las_pruebas)} pruebas pasaron.")
    print("TODAS LAS PRUEBAS PASARON" if pruebas_ejecutadas == len(todas_las_pruebas) else "HUBO FALLOS")


if __name__ == "__main__":
    main()
