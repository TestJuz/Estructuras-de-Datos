"""
main.py
-------
Programa principal que demuestra los 4 subtipos de árboles trabajados
en el curso, todos usando archivos para:
  1. Construir el árbol a partir de datos externos (archivo de entrada).
  2. Realizar operaciones típicas sobre cada estructura.
  3. Guardar (serializar) el árbol resultante a un archivo de salida.
  4. Recargar ese archivo y comprobar que el árbol se reconstruye
     correctamente (round-trip), demostrando que el ciclo
     guardar -> recargar preserva la información.

Ejecutar con:  python3 main.py
"""

import os
from arbol_general import ArbolGeneral
from arbol_binario import ArbolBinario
from arbol_bst import ArbolBST
from arbol_avl import ArbolAVL
import visualizador as viz

CARPETA_DATOS = "datos"
CARPETA_SALIDA = "salida"
CARPETA_IMAGENES = os.path.join(CARPETA_SALIDA, "imagenes")


def separador(titulo: str) -> None:
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def demo_arbol_general() -> None:
    separador("1. ÁRBOL GENERAL — estructura de carpetas de un proyecto")

    ruta_entrada = os.path.join(CARPETA_DATOS, "general.txt")
    ruta_salida = os.path.join(CARPETA_SALIDA, "general_guardado.txt")

    arbol = ArbolGeneral()
    arbol.cargar_desde_archivo(ruta_entrada)
    print(f"Árbol cargado desde '{ruta_entrada}':\n")
    arbol.mostrar()

    print(f"\nRecorrido preorden: {arbol.preorden()}")
    print(f"Cantidad de nodos: {arbol.contar_nodos()}")
    print(f"Altura del árbol: {arbol.altura()}")

    print("\nVista ASCII:")
    viz.mostrar_ascii(arbol.raiz, es_general=True)

    ruta_imagen = os.path.join(CARPETA_IMAGENES, "arbol_general.png")
    viz.dibujar_arbol_general(arbol.raiz, "Árbol General", ruta_imagen)
    print(f"\nImagen guardada en '{ruta_imagen}'")

    arbol.guardar_en_archivo(ruta_salida)
    print(f"\nÁrbol guardado en '{ruta_salida}'")

    # Recargar para comprobar que el archivo guardado es válido
    arbol_recargado = ArbolGeneral()
    arbol_recargado.cargar_desde_archivo(ruta_salida)
    coincide = arbol.preorden() == arbol_recargado.preorden()
    print(f"Verificación round-trip (guardar -> recargar): {'OK' if coincide else 'FALLÓ'}")


def demo_arbol_binario() -> None:
    separador("2. ÁRBOL BINARIO — recorridos clásicos")

    ruta_entrada = os.path.join(CARPETA_DATOS, "binario.txt")
    ruta_salida = os.path.join(CARPETA_SALIDA, "binario_guardado.txt")

    arbol = ArbolBinario()
    arbol.cargar_desde_archivo(ruta_entrada)
    print(f"Árbol cargado desde '{ruta_entrada}'")

    print(f"\nPreorden:   {arbol.preorden()}")
    print(f"Inorden:    {arbol.inorden()}")
    print(f"Postorden:  {arbol.postorden()}")
    print(f"Por niveles:{arbol.por_niveles()}")
    print(f"Altura: {arbol.altura()}")

    print("\nVista ASCII:")
    viz.mostrar_ascii(arbol.raiz)

    ruta_imagen = os.path.join(CARPETA_IMAGENES, "arbol_binario.png")
    viz.dibujar_arbol_binario(arbol.raiz, "Árbol Binario", ruta_imagen)
    print(f"\nImagen guardada en '{ruta_imagen}'")

    arbol.guardar_en_archivo(ruta_salida)
    print(f"\nÁrbol guardado en '{ruta_salida}'")

    arbol_recargado = ArbolBinario()
    arbol_recargado.cargar_desde_archivo(ruta_salida)
    coincide = arbol.por_niveles() == arbol_recargado.por_niveles()
    print(f"Verificación round-trip (guardar -> recargar): {'OK' if coincide else 'FALLÓ'}")

    arbol.destruir()
    print("Árbol liberado con destruir() (recorrido postorden).")


def demo_arbol_bst() -> None:
    separador("3. ÁRBOL BINARIO DE BÚSQUEDA (BST)")

    ruta_entrada = os.path.join(CARPETA_DATOS, "bst.txt")
    ruta_salida = os.path.join(CARPETA_SALIDA, "bst_guardado.txt")

    arbol = ArbolBST()
    arbol.cargar_desde_archivo(ruta_entrada)
    print(f"Árbol construido insertando valores de '{ruta_entrada}'")
    print(f"\nInorden (debe salir ordenado): {arbol.inorden()}")
    print(f"Altura: {arbol.altura()}")
    print(f"¿Es un BST válido?: {arbol.es_valido_bst()}")

    for valor in (7, 99):
        print(f"¿Existe {valor}? {arbol.buscar(valor)}")

    print("\nEliminando el valor 10 (nodo con dos hijos)...")
    arbol.eliminar(10)
    print(f"Inorden tras eliminar: {arbol.inorden()}")
    print(f"¿Sigue siendo válido?: {arbol.es_valido_bst()}")

    print("\nVista ASCII (tras eliminar):")
    viz.mostrar_ascii(arbol.raiz)

    ruta_imagen = os.path.join(CARPETA_IMAGENES, "arbol_bst.png")
    viz.dibujar_arbol_binario(arbol.raiz, "Árbol Binario de Búsqueda (BST)", ruta_imagen)
    print(f"\nImagen guardada en '{ruta_imagen}'")

    arbol.guardar_en_archivo(ruta_salida)
    print(f"\nÁrbol guardado (forma exacta) en '{ruta_salida}'")

    arbol_recargado = ArbolBST()
    arbol_recargado.cargar_forma_exacta_desde_archivo(ruta_salida)
    coincide = arbol.inorden() == arbol_recargado.inorden()
    print(f"Verificación round-trip (guardar -> recargar): {'OK' if coincide else 'FALLÓ'}")


def demo_arbol_avl() -> None:
    separador("4. ÁRBOL BALANCEADO (AVL)")

    ruta_entrada = os.path.join(CARPETA_DATOS, "avl.txt")
    ruta_salida = os.path.join(CARPETA_SALIDA, "avl_guardado.txt")

    arbol = ArbolAVL()
    arbol.cargar_desde_archivo(ruta_entrada)
    print(f"Árbol AVL construido insertando valores de '{ruta_entrada}'")
    print("(en un BST normal, este orden de inserción casi produce una lista)\n")

    arbol.mostrar_factores_balance()
    print(f"\nInorden: {arbol.inorden()}")
    print(f"Altura: {arbol.altura()}  (mucho menor que n-1 gracias al balance)")
    print(f"¿Está balanceado? (todos los factores en [-1, 1]): {arbol.esta_balanceado()}")

    print("\nVista ASCII:")
    viz.mostrar_ascii(arbol.raiz)

    # Recolecta el factor de balance de cada nodo para mostrarlo en la imagen
    etiquetas = {}

    def _recolectar(nodo):
        if nodo is None:
            return
        etiquetas[id(nodo)] = f"fb={arbol.obtener_factor_balance(nodo):+d}"
        _recolectar(nodo.izquierdo)
        _recolectar(nodo.derecho)

    _recolectar(arbol.raiz)

    ruta_imagen = os.path.join(CARPETA_IMAGENES, "arbol_avl.png")
    viz.dibujar_arbol_binario(arbol.raiz, "Árbol AVL (con factor de balance)", ruta_imagen, etiquetas_extra=etiquetas)
    print(f"\nImagen guardada en '{ruta_imagen}'")

    arbol.guardar_en_archivo(ruta_salida)
    print(f"\nÁrbol guardado en '{ruta_salida}'")

    arbol_recargado = ArbolAVL()
    arbol_recargado.cargar_forma_exacta_desde_archivo(ruta_salida)
    coincide = arbol.inorden() == arbol_recargado.inorden()
    print(f"Verificación round-trip (guardar -> recargar): {'OK' if coincide else 'FALLÓ'}")


def main() -> None:
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)

    demo_arbol_general()
    demo_arbol_binario()
    demo_arbol_bst()
    demo_arbol_avl()

    separador("Fin de la demostración")
    print("Revisa la carpeta 'salida/' para ver los archivos generados.")


if __name__ == "__main__":
    main()
