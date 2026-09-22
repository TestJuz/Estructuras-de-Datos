"""
arbol_avl.py
------------
Implementación de un Árbol AVL (árbol binario de búsqueda que se
autobalancea mediante rotaciones), con soporte para:
  - Construirlo insertando, en orden, una lista de valores leída de un
    archivo (demuestra que, sin importar el orden de entrada, el árbol
    se mantiene balanceado).
  - Guardar (serializar) el árbol a un archivo, preservando su forma
    exacta.
  - Ver el factor de balance de cada nodo.

Formato del archivo de ENTRADA (una sola línea, valores separados por
comas, en el orden en que deben insertarse):
    10,20,30,40,50,25

Con este archivo, un BST normal se degeneraría en una lista (10 < 20 <
30 < 40...), pero el árbol AVL se reequilibra automáticamente con
rotaciones — exactamente el problema y la solución explicados en la
presentación de Árboles Balanceados.
"""

from __future__ import annotations
from collections import deque

MARCADOR_NULO = "-"


class NodoAVL:
    """Nodo de un árbol AVL: dato, hijos y su propia altura (se
    necesita guardar la altura en cada nodo para calcular el factor de
    balance en O(1) sin recorrer todo el subárbol cada vez)."""

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo: "NodoAVL" | None = None
        self.derecho: "NodoAVL" | None = None
        self.altura = 0  # un nodo hoja tiene altura 0


class ArbolAVL:
    """Árbol AVL con inserción autobalanceada y operaciones de archivo."""

    def __init__(self):
        self.raiz: NodoAVL | None = None

    # ------------------------------------------------------------------
    # Utilidades de altura y balance
    # ------------------------------------------------------------------
    @staticmethod
    def _altura(nodo: NodoAVL | None) -> int:
        return nodo.altura if nodo is not None else -1

    def _actualizar_altura(self, nodo: NodoAVL) -> None:
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def _factor_balance(self, nodo: NodoAVL | None) -> int:
        """factor = altura(derecho) - altura(izquierdo).
        Si |factor| > 1, el nodo está desbalanceado y necesita rotar."""
        if nodo is None:
            return 0
        return self._altura(nodo.derecho) - self._altura(nodo.izquierdo)

    def obtener_factor_balance(self, nodo: NodoAVL) -> int:
        """Versión pública de _factor_balance(), pensada para que
        herramientas externas (como visualizador.py) puedan consultar
        el factor de balance de un nodo sin acceder a un método
        "privado" por convención."""
        return self._factor_balance(nodo)

    # ------------------------------------------------------------------
    # Rotaciones (las 4 vistas en la presentación)
    # ------------------------------------------------------------------
    def _rotacion_derecha(self, y: NodoAVL) -> NodoAVL:
        """Rotación simple a la derecha (caso Izquierda-Izquierda)."""
        x = y.izquierdo
        t2 = x.derecho

        x.derecho = y
        y.izquierdo = t2

        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x  # x es la nueva raíz de este subárbol

    def _rotacion_izquierda(self, x: NodoAVL) -> NodoAVL:
        """Rotación simple a la izquierda (caso Derecha-Derecha)."""
        y = x.derecho
        t2 = y.izquierdo

        y.izquierdo = x
        x.derecho = t2

        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y  # y es la nueva raíz de este subárbol

    def _rebalancear(self, nodo: NodoAVL) -> NodoAVL:
        """Revisa el factor de balance de un nodo y aplica la rotación
        (simple o doble) que corresponda."""
        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        # Caso Izquierda-Izquierda o Izquierda-Derecha
        if balance < -1:
            if self._factor_balance(nodo.izquierdo) > 0:
                nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)  # LR -> LL
            return self._rotacion_derecha(nodo)

        # Caso Derecha-Derecha o Derecha-Izquierda
        if balance > 1:
            if self._factor_balance(nodo.derecho) < 0:
                nodo.derecho = self._rotacion_derecha(nodo.derecho)  # RL -> RR
            return self._rotacion_izquierda(nodo)

        return nodo  # ya estaba balanceado

    # ------------------------------------------------------------------
    # Inserción autobalanceada
    # ------------------------------------------------------------------
    def insertar(self, valor) -> None:
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo: NodoAVL | None, valor) -> NodoAVL:
        if nodo is None:
            return NodoAVL(valor)

        if valor < nodo.dato:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.dato:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor)
        else:
            return nodo  # duplicado, no se inserta

        return self._rebalancear(nodo)

    # ------------------------------------------------------------------
    # Búsqueda
    # ------------------------------------------------------------------
    def buscar(self, valor) -> bool:
        nodo = self.raiz
        while nodo is not None:
            if valor == nodo.dato:
                return True
            nodo = nodo.izquierdo if valor < nodo.dato else nodo.derecho
        return False

    # ------------------------------------------------------------------
    # Carga desde archivo (inserciones en orden, con rebalanceo)
    # ------------------------------------------------------------------
    def cargar_desde_archivo(self, ruta: str) -> None:
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
    # Guardado y recarga (forma exacta, por niveles)
    # ------------------------------------------------------------------
    def guardar_en_archivo(self, ruta: str) -> None:
        if self.raiz is None:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("# Árbol AVL vacío\n")
                archivo.write(MARCADOR_NULO + "\n")
            return

        valores: list[str] = []
        cola: deque[NodoAVL | None] = deque([self.raiz])
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
            archivo.write("# Árbol AVL serializado por niveles (ya balanceado)\n")
            archivo.write(",".join(valores) + "\n")

    def cargar_forma_exacta_desde_archivo(self, ruta: str) -> None:
        """Reconstruye el árbol AVL a partir de un archivo guardado con
        guardar_en_archivo(), preservando la forma EXACTA (por niveles,
        igual que ArbolBinario), recalculando la altura de cada nodo
        de abajo hacia arriba al terminar."""
        with open(ruta, "r", encoding="utf-8") as archivo:
            linea = self._leer_primera_linea_util(archivo)

        if linea is None:
            raise ValueError(f"El archivo '{ruta}' no contiene datos válidos")

        valores = [v.strip() for v in linea.split(",")]
        if not valores or valores[0] == MARCADOR_NULO:
            self.raiz = None
            return

        self.raiz = NodoAVL(self._convertir(valores[0]))
        cola: deque[NodoAVL] = deque([self.raiz])
        i = 1
        while cola and i < len(valores):
            actual = cola.popleft()
            if i < len(valores):
                v = valores[i]; i += 1
                if v != MARCADOR_NULO:
                    actual.izquierdo = NodoAVL(self._convertir(v))
                    cola.append(actual.izquierdo)
            if i < len(valores):
                v = valores[i]; i += 1
                if v != MARCADOR_NULO:
                    actual.derecho = NodoAVL(self._convertir(v))
                    cola.append(actual.derecho)

        self._recalcular_alturas(self.raiz)

    def _recalcular_alturas(self, nodo: NodoAVL | None) -> int:
        """Recalcula recursivamente la altura de cada nodo (necesario
        tras cargar por niveles, ya que esa carga no actualiza el
        campo .altura como sí lo hace insertar())."""
        if nodo is None:
            return -1
        izq = self._recalcular_alturas(nodo.izquierdo)
        der = self._recalcular_alturas(nodo.derecho)
        nodo.altura = 1 + max(izq, der)
        return nodo.altura

    # ------------------------------------------------------------------
    # Recorridos y utilidades
    # ------------------------------------------------------------------
    def inorden(self) -> list:
        resultado: list = []

        def recorrer(nodo: NodoAVL | None) -> None:
            if nodo is None:
                return
            recorrer(nodo.izquierdo)
            resultado.append(nodo.dato)
            recorrer(nodo.derecho)

        recorrer(self.raiz)
        return resultado

    def altura(self) -> int:
        return self._altura(self.raiz)

    def esta_balanceado(self) -> bool:
        """Verifica que TODOS los nodos cumplan |factor de balance| <= 1
        (una comprobación externa, independiente del proceso de
        inserción, útil para validar la corrección del algoritmo)."""

        def verificar(nodo: NodoAVL | None) -> bool:
            if nodo is None:
                return True
            if abs(self._factor_balance(nodo)) > 1:
                return False
            return verificar(nodo.izquierdo) and verificar(nodo.derecho)

        return verificar(self.raiz)

    def mostrar_factores_balance(self) -> None:
        """Imprime cada nodo con su factor de balance, para fines
        didácticos (ver visualmente que ningún nodo excede ±1)."""

        def imprimir(nodo: NodoAVL | None, nivel: int) -> None:
            if nodo is None:
                return
            fb = self._factor_balance(nodo)
            print("  " * nivel + f"- {nodo.dato}  (altura={nodo.altura}, factor={fb:+d})")
            imprimir(nodo.izquierdo, nivel + 1)
            imprimir(nodo.derecho, nivel + 1)

        imprimir(self.raiz, 0)


if __name__ == "__main__":
    arbol = ArbolAVL()
    # Insertar en orden ascendente degeneraría un BST normal en una lista.
    for valor in [10, 20, 30, 40, 50, 25]:
        arbol.insertar(valor)

    arbol.mostrar_factores_balance()
    print("Inorden:", arbol.inorden())
    print("Altura:", arbol.altura())
    print("¿Está balanceado?", arbol.esta_balanceado())
