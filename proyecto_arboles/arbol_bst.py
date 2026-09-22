"""
arbol_bst.py
------------
Implementación de un Árbol Binario de Búsqueda (BST), con soporte para:
  - Construirlo insertando, en orden, una lista de valores leída de un
    archivo (demuestra el algoritmo de inserción visto en clase).
  - Guardar (serializar) el árbol a un archivo, preservando su forma
    EXACTA (no solo los valores), para poder recargarlo sin que la
    estructura cambie.
  - Buscar, insertar y eliminar (con los 3 casos clásicos).

Formato del archivo de ENTRADA para construir el árbol por inserciones
(una sola línea, valores separados por comas, en el orden en que deben
insertarse):
    8,3,10,1,6,14,4,7

Formato del archivo de SALIDA al guardar: recorrido por niveles con
"-" para huecos (el mismo formato que arbol_binario.py), porque es la
única forma de preservar la forma exacta del árbol al recargarlo.
"""

from __future__ import annotations
from collections import deque

MARCADOR_NULO = "-"


class NodoBST:
    """Nodo de un árbol binario de búsqueda."""

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo: "NodoBST" | None = None
        self.derecho: "NodoBST" | None = None


class ArbolBST:
    """Árbol Binario de Búsqueda con operaciones de archivo."""

    def __init__(self):
        self.raiz: NodoBST | None = None

    # ------------------------------------------------------------------
    # Inserción, búsqueda, eliminación
    # ------------------------------------------------------------------
    def insertar(self, valor) -> None:
        """Inserta un valor manteniendo la propiedad de orden del BST:
        izquierda < nodo < derecha. Ignora silenciosamente duplicados,
        como se explicó en la presentación (comportamiento típico de
        un BST simple)."""
        if self.raiz is None:
            self.raiz = NodoBST(valor)
            return
        self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo: NodoBST, valor) -> None:
        if valor < nodo.dato:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.dato:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)
        # valor == nodo.dato -> duplicado, no se inserta

    def buscar(self, valor) -> bool:
        """Devuelve True si el valor existe en el árbol. O(altura)."""
        nodo = self.raiz
        while nodo is not None:
            if valor == nodo.dato:
                return True
            nodo = nodo.izquierdo if valor < nodo.dato else nodo.derecho
        return False

    def eliminar(self, valor) -> None:
        """Elimina un valor del árbol, manejando los 3 casos clásicos
        (hoja, un hijo, dos hijos) exactamente como en la presentación
        de BST."""
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo: NodoBST | None, valor) -> NodoBST | None:
        if nodo is None:
            return None  # el valor no estaba en el árbol

        if valor < nodo.dato:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.dato:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            # Caso 1: nodo hoja
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            # Caso 2: un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: dos hijos -> reemplazar con el sucesor
            # (el menor del subárbol derecho)
            sucesor = nodo.derecho
            while sucesor.izquierdo is not None:
                sucesor = sucesor.izquierdo
            nodo.dato = sucesor.dato
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.dato)

        return nodo

    # ------------------------------------------------------------------
    # Carga desde archivo (lista de valores a insertar en orden)
    # ------------------------------------------------------------------
    def cargar_desde_archivo(self, ruta: str) -> None:
        """Construye el BST insertando, en orden, los valores listados
        en el archivo. El orden de inserción determina la forma final
        del árbol (como se explicó en la diapositiva del caso
        degenerado: insertar datos ya ordenados produce un árbol
        equivalente a una lista)."""
        self.raiz = None

        with open(ruta, "r", encoding="utf-8") as archivo:
            linea = self._leer_primera_linea_util(archivo)

        if linea is None:
            raise ValueError(f"El archivo '{ruta}' no contiene datos válidos")

        for valor_str in linea.split(","):
            valor_str = valor_str.strip()
            if valor_str:
                self.insertar(self._convertir(valor_str))

    @staticmethod
    def _leer_primera_linea_util(archivo) -> str | None:
        for linea in archivo:
            linea = linea.strip()
            if linea and not linea.startswith("#"):
                return linea
        return None

    @staticmethod
    def _convertir(valor: str):
        try:
            return int(valor)
        except ValueError:
            return valor

    # ------------------------------------------------------------------
    # Guardado a archivo (preserva la forma exacta, no solo los valores)
    # ------------------------------------------------------------------
    def guardar_en_archivo(self, ruta: str) -> None:
        """Serializa el árbol por niveles, igual que arbol_binario.py.
        Esto es importante: si guardáramos solo los valores en
        inorden, al recargar (reinsertando) obtendríamos SIEMPRE la
        misma forma sin importar la forma original, perdiendo
        información sobre rotaciones o el orden de inserción real."""
        if self.raiz is None:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("# BST vacío\n")
                archivo.write(MARCADOR_NULO + "\n")
            return

        valores: list[str] = []
        cola: deque[NodoBST | None] = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            if nodo is None:
                valores.append(MARCADOR_NULO)
                continue
            valores.append(str(nodo.dato))
            cola.append(nodo.izquierdo)
            cola.append(nodo.derecho)

        while valores and valores[-1] == MARCADOR_NULO:
            valores.pop()

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("# BST serializado por niveles (preserva la forma exacta)\n")
            archivo.write(",".join(valores) + "\n")

    def cargar_forma_exacta_desde_archivo(self, ruta: str) -> None:
        """Reconstruye el árbol a partir de un archivo guardado con
        guardar_en_archivo(), preservando la forma EXACTA (usa el
        mismo algoritmo por niveles que arbol_binario.py, en vez de
        reinsertar valores)."""
        with open(ruta, "r", encoding="utf-8") as archivo:
            linea = self._leer_primera_linea_util(archivo)

        if linea is None:
            raise ValueError(f"El archivo '{ruta}' no contiene datos válidos")

        valores = [v.strip() for v in linea.split(",")]
        if not valores or valores[0] == MARCADOR_NULO:
            self.raiz = None
            return

        self.raiz = NodoBST(self._convertir(valores[0]))
        cola: deque[NodoBST] = deque([self.raiz])
        i = 1
        while cola and i < len(valores):
            actual = cola.popleft()
            if i < len(valores):
                v = valores[i]; i += 1
                if v != MARCADOR_NULO:
                    actual.izquierdo = NodoBST(self._convertir(v))
                    cola.append(actual.izquierdo)
            if i < len(valores):
                v = valores[i]; i += 1
                if v != MARCADOR_NULO:
                    actual.derecho = NodoBST(self._convertir(v))
                    cola.append(actual.derecho)

    # ------------------------------------------------------------------
    # Recorridos y utilidades
    # ------------------------------------------------------------------
    def inorden(self) -> list:
        """El inorden de un BST siempre da los valores ordenados —
        útil como verificación de que la propiedad de orden se cumple."""
        resultado: list = []

        def recorrer(nodo: NodoBST | None) -> None:
            if nodo is None:
                return
            recorrer(nodo.izquierdo)
            resultado.append(nodo.dato)
            recorrer(nodo.derecho)

        recorrer(self.raiz)
        return resultado

    def altura(self) -> int:
        def altura_nodo(nodo: NodoBST | None) -> int:
            if nodo is None:
                return -1
            return 1 + max(altura_nodo(nodo.izquierdo), altura_nodo(nodo.derecho))

        return altura_nodo(self.raiz)

    def es_valido_bst(self) -> bool:
        """Verifica que la propiedad de orden se cumpla en todo el
        árbol (útil para validar árboles cargados desde un archivo
        externo no confiable, ver sección de seguridad)."""
        valores = self.inorden()
        return all(valores[i] < valores[i + 1] for i in range(len(valores) - 1))


if __name__ == "__main__":
    arbol = ArbolBST()
    for valor in [8, 3, 10, 1, 6, 14, 4, 7]:
        arbol.insertar(valor)

    print("Inorden (debe salir ordenado):", arbol.inorden())
    print("Altura:", arbol.altura())
    print("¿Existe 7?", arbol.buscar(7))
    print("¿Existe 99?", arbol.buscar(99))
    arbol.eliminar(3)
    print("Inorden tras eliminar 3:", arbol.inorden())
    print("¿Es BST válido?", arbol.es_valido_bst())
