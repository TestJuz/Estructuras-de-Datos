"""
visualizador.py
----------------
Genera diagramas visuales (imágenes .png) de los árboles del proyecto,
usando matplotlib. Sirve para los 4 tipos:

  - Árboles binarios, BST y AVL: comparten la misma forma de nodo
    (dato, izquierdo, derecho), así que se dibujan con una sola
    función genérica: dibujar_arbol_binario().
  - Árboles generales (N hijos por nodo): se dibujan con
    dibujar_arbol_general().

También incluye mostrar_ascii(), una vista rápida en texto (con líneas
de conexión) para cuando no se necesita/puede abrir una imagen.

Requiere matplotlib:  pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")  # No necesita una ventana gráfica para GUARDAR el .png
import matplotlib.pyplot as plt


# ======================================================================
# ÁRBOLES BINARIOS / BST / AVL  (nodo.dato, nodo.izquierdo, nodo.derecho)
# ======================================================================

def _asignar_posiciones_binario(nodo, profundidad, contador, posiciones):
    """Recorrido INORDEN para asignar la posición X: así, un BST se
    dibuja automáticamente con los valores en orden creciente de
    izquierda a derecha (igual que en las diapositivas)."""
    if nodo is None:
        return
    ESPACIADO_VERTICAL = 1.3  # más espacio entre niveles para etiquetas extra
    _asignar_posiciones_binario(nodo.izquierdo, profundidad + 1, contador, posiciones)
    x = contador[0]
    contador[0] += 1
    posiciones[id(nodo)] = (x, -profundidad * ESPACIADO_VERTICAL)
    _asignar_posiciones_binario(nodo.derecho, profundidad + 1, contador, posiciones)


def dibujar_arbol_binario(raiz, titulo, ruta_salida, etiquetas_extra=None):
    """Dibuja un árbol binario/BST/AVL y guarda el resultado como PNG.

    etiquetas_extra: dict opcional {id(nodo): "texto"} para mostrar un
    dato adicional bajo cada nodo (por ejemplo, el factor de balance
    en un AVL).
    """
    etiquetas_extra = etiquetas_extra or {}
    posiciones = {}
    _asignar_posiciones_binario(raiz, 0, [0], posiciones)

    fig, ax = plt.subplots(figsize=(max(6, len(posiciones) * 0.9), 5))

    # Dibuja las aristas primero (para que queden detrás de los círculos)
    def dibujar_aristas(nodo):
        if nodo is None:
            return
        x1, y1 = posiciones[id(nodo)]
        for hijo in (nodo.izquierdo, nodo.derecho):
            if hijo is not None:
                x2, y2 = posiciones[id(hijo)]
                ax.plot([x1, x2], [y1, y2], color="#999999", zorder=1, linewidth=1.5)
                dibujar_aristas(hijo)

    dibujar_aristas(raiz)

    # Dibuja los nodos (círculos con el dato adentro)
    def dibujar_nodos(nodo):
        if nodo is None:
            return
        x, y = posiciones[id(nodo)]
        circulo = plt.Circle((x, y), 0.4, facecolor="#A9CCE3", edgecolor="#555555", zorder=2)
        ax.add_patch(circulo)
        ax.text(x, y, str(nodo.dato), ha="center", va="center", fontsize=11, fontweight="bold", zorder=3)
        if id(nodo) in etiquetas_extra:
            ax.text(x, y - 0.45, etiquetas_extra[id(nodo)], ha="center", va="top", fontsize=8.5, color="#C0392B", zorder=3)
        dibujar_nodos(nodo.izquierdo)
        dibujar_nodos(nodo.derecho)

    dibujar_nodos(raiz)

    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.set_xlim(-1, contador_maximo(posiciones) + 1)
    ax.set_ylim(min(y for _, y in posiciones.values()) - 1, 1)
    ax.axis("off")
    ax.set_aspect("equal")
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=130)
    plt.close(fig)


def contador_maximo(posiciones):
    return max((x for x, _ in posiciones.values()), default=0)


# ======================================================================
# ÁRBOLES GENERALES  (nodo.dato, nodo.hijos = lista)
# ======================================================================

def _asignar_posiciones_general(nodo, profundidad, contador, posiciones):
    ESPACIADO = 1.7  # separa más los nodos hoja para que quepan etiquetas largas
    if not nodo.hijos:
        x = contador[0] * ESPACIADO
        contador[0] += 1
        posiciones[id(nodo)] = (x, -profundidad)
        return x

    xs_hijos = [
        _asignar_posiciones_general(hijo, profundidad + 1, contador, posiciones)
        for hijo in nodo.hijos
    ]
    x = sum(xs_hijos) / len(xs_hijos)  # centrado sobre sus hijos
    posiciones[id(nodo)] = (x, -profundidad)
    return x


def dibujar_arbol_general(raiz, titulo, ruta_salida):
    """Dibuja un árbol general (N hijos por nodo) y guarda un PNG."""
    posiciones = {}
    _asignar_posiciones_general(raiz, 0, [0], posiciones)

    fig, ax = plt.subplots(figsize=(max(7, len(posiciones) * 0.85), 5))

    def dibujar_aristas(nodo):
        x1, y1 = posiciones[id(nodo)]
        for hijo in nodo.hijos:
            x2, y2 = posiciones[id(hijo)]
            ax.plot([x1, x2], [y1, y2], color="#999999", zorder=1, linewidth=1.5)
            dibujar_aristas(hijo)

    dibujar_aristas(raiz)

    def dibujar_nodos(nodo):
        x, y = posiciones[id(nodo)]
        ancho = min(1.5, 0.35 + 0.1 * len(str(nodo.dato)))
        caja = plt.Rectangle((x - ancho / 2, y - 0.22), ancho, 0.44,
                              facecolor="#A8D8B9", edgecolor="#555555", zorder=2)
        ax.add_patch(caja)
        ax.text(x, y, str(nodo.dato), ha="center", va="center", fontsize=9.5, fontweight="bold", zorder=3)
        for hijo in nodo.hijos:
            dibujar_nodos(hijo)

    dibujar_nodos(raiz)

    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.set_xlim(-1, contador_maximo(posiciones) + 1)
    ax.set_ylim(min(y for _, y in posiciones.values()) - 1, 1)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=130)
    plt.close(fig)


# ======================================================================
# VISTA RÁPIDA EN TEXTO (sin dependencias, para la terminal)
# ======================================================================

def mostrar_ascii(nodo, prefijo="", es_ultimo=True, es_general=False):
    """Imprime el árbol en la terminal usando líneas ASCII, similar al
    comando 'tree' de la consola. Funciona tanto para nodos binarios
    (izquierdo/derecho) como generales (hijos), sin necesitar
    matplotlib ni generar ningún archivo."""
    if nodo is None:
        return

    conector = "└── " if es_ultimo else "├── "
    print(prefijo + conector + str(nodo.dato))
    prefijo_hijo = prefijo + ("    " if es_ultimo else "│   ")

    if es_general:
        hijos = nodo.hijos
    else:
        hijos = [h for h in (nodo.izquierdo, nodo.derecho) if h is not None]

    for i, hijo in enumerate(hijos):
        mostrar_ascii(hijo, prefijo_hijo, i == len(hijos) - 1, es_general)
