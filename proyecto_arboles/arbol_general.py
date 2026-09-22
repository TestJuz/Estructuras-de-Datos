"""
arbol_general.py
-----------------
Implementación de un Árbol General (cada nodo puede tener cualquier
cantidad de hijos), con soporte para:
  - Construir el árbol leyendo relaciones padre-hijo desde un archivo.
  - Guardar (serializar) el árbol a un archivo de texto.
  - Recorridos y utilidades básicas (altura, conteo de nodos).

Formato del archivo de entrada (texto plano, una relación por línea):
    ROOT,A
    A,B
    A,C
    B,D

La primera columna es el padre ("ROOT" indica que el segundo valor es
la raíz del árbol, es decir, no tiene padre). La segunda columna es el
hijo. Las líneas vacías o que empiezan con "#" se ignoran (comentarios).
"""

from __future__ import annotations


class NodoGeneral:
    """Nodo de un árbol general: un dato y una lista dinámica de hijos."""

    def __init__(self, dato):
        self.dato = dato
        self.hijos: list["NodoGeneral"] = []

    def agregar_hijo(self, hijo: "NodoGeneral") -> None:
        self.hijos.append(hijo)

    def __repr__(self) -> str:
        return f"NodoGeneral({self.dato!r})"


class ArbolGeneral:
    """Árbol general con operaciones de carga/guardado desde archivo."""

    def __init__(self):
        self.raiz: NodoGeneral | None = None
        # Índice auxiliar dato -> nodo, para reconstruir relaciones
        # padre-hijo en O(1) al leer el archivo.
        self._indice: dict = {}

    # ------------------------------------------------------------------
    # Construcción manual (sin archivo)
    # ------------------------------------------------------------------
    def insertar(self, dato_padre, dato_hijo) -> None:
        """Inserta dato_hijo como hijo de dato_padre. Si dato_padre es
        None, dato_hijo se convierte en la raíz del árbol."""
        nodo_hijo = self._obtener_o_crear(dato_hijo)

        if dato_padre is None:
            self.raiz = nodo_hijo
            return

        nodo_padre = self._obtener_o_crear(dato_padre)
        nodo_padre.agregar_hijo(nodo_hijo)

    def _obtener_o_crear(self, dato) -> NodoGeneral:
        if dato not in self._indice:
            self._indice[dato] = NodoGeneral(dato)
        return self._indice[dato]

    # ------------------------------------------------------------------
    # Carga desde archivo
    # ------------------------------------------------------------------
    def cargar_desde_archivo(self, ruta: str) -> None:
        """Construye el árbol leyendo relaciones padre-hijo desde un
        archivo de texto. Lanza ValueError si el archivo está mal
        formado (buena práctica: validar entradas externas antes de
        confiar en ellas, como se discutió en la sección de seguridad
        de las diapositivas de Árboles)."""
        self.raiz = None
        self._indice = {}

        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue

                partes = linea.split(",")
                if len(partes) != 2:
                    raise ValueError(
                        f"Línea {numero_linea} mal formada en '{ruta}': "
                        f"se esperaba 'padre,hijo', se obtuvo '{linea}'"
                    )

                padre_str, hijo_str = (p.strip() for p in partes)

                if padre_str == "ROOT":
                    nodo_raiz = self._obtener_o_crear(hijo_str)
                    self.raiz = nodo_raiz
                else:
                    self.insertar(padre_str, hijo_str)

        if self.raiz is None:
            raise ValueError(
                f"El archivo '{ruta}' no define una raíz (línea 'ROOT,<valor>')"
            )

    # ------------------------------------------------------------------
    # Guardado a archivo
    # ------------------------------------------------------------------
    def guardar_en_archivo(self, ruta: str) -> None:
        """Serializa el árbol al mismo formato padre-hijo, de modo que
        pueda volver a cargarse con cargar_desde_archivo()."""
        if self.raiz is None:
            raise ValueError("No se puede guardar un árbol vacío")

        lineas = [f"ROOT,{self.raiz.dato}"]

        def recorrer(nodo: NodoGeneral) -> None:
            for hijo in nodo.hijos:
                lineas.append(f"{nodo.dato},{hijo.dato}")
                recorrer(hijo)

        recorrer(self.raiz)

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("# Árbol general serializado automáticamente\n")
            archivo.write("\n".join(lineas) + "\n")

    # ------------------------------------------------------------------
    # Recorridos y utilidades
    # ------------------------------------------------------------------
    def preorden(self) -> list:
        """Recorrido preorden: visita el nodo antes que a sus hijos."""
        resultado: list = []

        def recorrer(nodo: NodoGeneral | None) -> None:
            if nodo is None:
                return
            resultado.append(nodo.dato)
            for hijo in nodo.hijos:
                recorrer(hijo)

        recorrer(self.raiz)
        return resultado

    def altura(self) -> int:
        """Altura del árbol (0 para un único nodo, -1 para árbol vacío)."""

        def altura_nodo(nodo: NodoGeneral | None) -> int:
            if nodo is None:
                return -1
            if not nodo.hijos:
                return 0
            return 1 + max(altura_nodo(h) for h in nodo.hijos)

        return altura_nodo(self.raiz)

    def contar_nodos(self) -> int:
        return len(self.preorden())

    def mostrar(self) -> None:
        """Imprime el árbol en forma de jerarquía indentada."""

        def imprimir(nodo: NodoGeneral | None, nivel: int) -> None:
            if nodo is None:
                return
            print("  " * nivel + f"- {nodo.dato}")
            for hijo in nodo.hijos:
                imprimir(hijo, nivel + 1)

        imprimir(self.raiz, 0)


if __name__ == "__main__":
    # Prueba rápida manual (no requiere archivo)
    arbol = ArbolGeneral()
    arbol.insertar(None, "A")
    arbol.insertar("A", "B")
    arbol.insertar("A", "C")
    arbol.insertar("B", "D")
    arbol.mostrar()
    print("Preorden:", arbol.preorden())
    print("Altura:", arbol.altura())
