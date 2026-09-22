"""
arbol_binario.py
-----------------
Implementación de un Árbol Binario genérico (cada nodo tiene como
máximo 2 hijos: izquierdo y derecho, sin la propiedad de orden de un
BST), con soporte para:
  - Construir el árbol leyendo su recorrido por niveles desde un archivo.
  - Guardar (serializar) el árbol a un archivo de texto.
  - Recorridos: preorden, inorden, postorden y por niveles.

Formato del archivo de entrada (una sola línea, valores separados por
comas, recorrido POR NIVELES; "-" representa un hijo ausente/NULL):
    8,3,10,1,6,-,14

Este formato es el mismo que usan muchas plataformas de ejercicios de
programación (LeetCode, HackerRank) para representar árboles binarios
de forma compacta y sin ambigüedad.
"""

from __future__ import annotations
from collections import deque


class NodoBinario:
    """Nodo de un árbol binario: dato, hijo izquierdo e hijo derecho."""

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo: "NodoBinario" | None = None
        self.derecho: "NodoBinario" | None = None

    def __repr__(self) -> str:
        return f"NodoBinario({self.dato!r})"


MARCADOR_NULO = "-"


class ArbolBinario:
    """Árbol binario con operaciones de carga/guardado desde archivo."""

    def __init__(self):
        self.raiz: NodoBinario | None = None

    # ------------------------------------------------------------------
    # Carga desde archivo
    # ------------------------------------------------------------------
    def cargar_desde_archivo(self, ruta: str) -> None:
        """Construye el árbol a partir de su recorrido por niveles,
        guardado como una sola línea de valores separados por comas.
        Usa una cola (igual que el algoritmo BFS de la presentación de
        Árboles) para ir asignando hijos izquierdo/derecho en orden."""
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = self._leer_primera_linea_util(archivo)

        if contenido is None:
            raise ValueError(f"El archivo '{ruta}' no contiene datos válidos")

        valores = [v.strip() for v in contenido.split(",")]
        if not valores or valores[0] == MARCADOR_NULO:
            self.raiz = None
            return

        self.raiz = NodoBinario(self._convertir(valores[0]))
        cola: deque[NodoBinario] = deque([self.raiz])
        i = 1

        while cola and i < len(valores):
            nodo_actual = cola.popleft()

            # Hijo izquierdo
            if i < len(valores):
                valor = valores[i]
                i += 1
                if valor != MARCADOR_NULO:
                    nodo_actual.izquierdo = NodoBinario(self._convertir(valor))
                    cola.append(nodo_actual.izquierdo)

            # Hijo derecho
            if i < len(valores):
                valor = valores[i]
                i += 1
                if valor != MARCADOR_NULO:
                    nodo_actual.derecho = NodoBinario(self._convertir(valor))
                    cola.append(nodo_actual.derecho)

    @staticmethod
    def _leer_primera_linea_util(archivo) -> str | None:
        """Devuelve la primera línea no vacía y que no sea comentario."""
        for linea in archivo:
            linea = linea.strip()
            if linea and not linea.startswith("#"):
                return linea
        return None

    @staticmethod
    def _convertir(valor: str):
        """Intenta convertir a int; si no es posible, deja el string tal
        cual (permite tanto árboles numéricos como de texto)."""
        try:
            return int(valor)
        except ValueError:
            return valor

    # ------------------------------------------------------------------
    # Guardado a archivo
    # ------------------------------------------------------------------
    def guardar_en_archivo(self, ruta: str) -> None:
        """Serializa el árbol por niveles (mismo formato que la carga),
        de modo que el archivo pueda volver a leerse sin pérdida de
        información sobre la forma exacta del árbol."""
        if self.raiz is None:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("# Árbol binario vacío\n")
                archivo.write(MARCADOR_NULO + "\n")
            return

        valores: list[str] = []
        cola: deque[NodoBinario | None] = deque([self.raiz])

        while cola:
            nodo = cola.popleft()
            if nodo is None:
                valores.append(MARCADOR_NULO)
                continue
            valores.append(str(nodo.dato))
            cola.append(nodo.izquierdo)
            cola.append(nodo.derecho)

        # Recorta los marcadores nulos finales (no aportan información,
        # y mantiene el archivo compacto y legible).
        while valores and valores[-1] == MARCADOR_NULO:
            valores.pop()

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("# Árbol binario serializado por niveles\n")
            archivo.write(",".join(valores) + "\n")

    # ------------------------------------------------------------------
    # Recorridos
    # ------------------------------------------------------------------
    def preorden(self) -> list:
        resultado: list = []

        def recorrer(nodo: NodoBinario | None) -> None:
            if nodo is None:
                return
            resultado.append(nodo.dato)
            recorrer(nodo.izquierdo)
            recorrer(nodo.derecho)

        recorrer(self.raiz)
        return resultado

    def inorden(self) -> list:
        resultado: list = []

        def recorrer(nodo: NodoBinario | None) -> None:
            if nodo is None:
                return
            recorrer(nodo.izquierdo)
            resultado.append(nodo.dato)
            recorrer(nodo.derecho)

        recorrer(self.raiz)
        return resultado

    def postorden(self) -> list:
        resultado: list = []

        def recorrer(nodo: NodoBinario | None) -> None:
            if nodo is None:
                return
            recorrer(nodo.izquierdo)
            recorrer(nodo.derecho)
            resultado.append(nodo.dato)

        recorrer(self.raiz)
        return resultado

    def por_niveles(self) -> list:
        """Recorrido BFS (por niveles), igual que en la presentación
        de Grafos/Árboles: usa una cola explícita, no recursión."""
        if self.raiz is None:
            return []

        resultado: list = []
        cola: deque[NodoBinario] = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.dato)
            if nodo.izquierdo is not None:
                cola.append(nodo.izquierdo)
            if nodo.derecho is not None:
                cola.append(nodo.derecho)
        return resultado

    def altura(self) -> int:
        def altura_nodo(nodo: NodoBinario | None) -> int:
            if nodo is None:
                return -1
            return 1 + max(altura_nodo(nodo.izquierdo), altura_nodo(nodo.derecho))

        return altura_nodo(self.raiz)

    def destruir(self) -> None:
        """Libera el árbol recorriendo en postorden (hijos antes que el
        nodo actual), tal como se explica en la sección de buenas
        prácticas de memoria de la presentación de Árboles Binarios.
        En Python el recolector de basura maneja la memoria, pero
        replicamos el patrón correcto por completitud pedagógica."""

        def liberar(nodo: NodoBinario | None) -> None:
            if nodo is None:
                return
            liberar(nodo.izquierdo)
            liberar(nodo.derecho)
            nodo.izquierdo = None
            nodo.derecho = None

        liberar(self.raiz)
        self.raiz = None


if __name__ == "__main__":
    arbol = ArbolBinario()
    arbol.raiz = NodoBinario(8)
    arbol.raiz.izquierdo = NodoBinario(3)
    arbol.raiz.derecho = NodoBinario(10)
    arbol.raiz.izquierdo.izquierdo = NodoBinario(1)
    arbol.raiz.izquierdo.derecho = NodoBinario(6)
    arbol.raiz.derecho.derecho = NodoBinario(14)

    print("Preorden:", arbol.preorden())
    print("Inorden:", arbol.inorden())
    print("Postorden:", arbol.postorden())
    print("Por niveles:", arbol.por_niveles())
    print("Altura:", arbol.altura())
