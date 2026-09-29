class NodoLibro:
    def __init__(self, codigo, titulo, disponibles):
        self.codigo = codigo
        self.titulo = titulo
        self.disponibles = disponibles
        self.izquierdo = None
        self.derecho = None
 
def insertar(raiz, codigo, titulo, disponibles):
    if raiz is None:
        return NodoLibro(codigo, titulo, disponibles)
    if codigo < raiz.codigo:
        raiz.izquierdo = insertar(raiz.izquierdo, codigo, titulo, disponibles)
    elif codigo > raiz.codigo:
        raiz.derecho = insertar(raiz.derecho, codigo, titulo, disponibles)
    else:
        raise ValueError(f'Código duplicado: {codigo}')
    return raiz
 
def cargar_catalogo(ruta):
    raiz = None
    with open(ruta, encoding='utf-8') as archivo:
        for numero, linea in enumerate(archivo, 1):
            if not linea.strip():
                continue
            partes = linea.strip().split('|')
            if len(partes) != 3:
                raise ValueError(f'Línea {numero} incorrecta')
            codigo, titulo, disponibles = partes
            if int(disponibles) < 0:
                raise ValueError(f'Inventario negativo en línea {numero}')
            raiz = insertar(raiz, int(codigo), titulo, int(disponibles))
    return raiz
 
raiz = cargar_catalogo('catalogo_libros.txt')
print('Raíz:', raiz.codigo)  # 410

def buscar(nodo, codigo):
    if nodo is None or nodo.codigo == codigo:
        return nodo
    if codigo < nodo.codigo:
        return buscar(nodo.izquierdo, codigo)
    return buscar(nodo.derecho, codigo)
 
def listado_inorden(nodo):
    if nodo is None:
        return []
    return (listado_inorden(nodo.izquierdo)
            + [(nodo.codigo, nodo.titulo, nodo.disponibles)]
            + listado_inorden(nodo.derecho))
 
print('Libro 330:', buscar(raiz, 330).titulo)
print('Código 999 registrado:', buscar(raiz, 999) is not None)
for libro in listado_inorden(raiz):
    print(libro)

def prestar(raiz, codigo):
    libro = buscar(raiz, codigo)
    if libro is None or libro.disponibles == 0:
        return False
    libro.disponibles -= 1
    return True

def devolver(raiz, codigo):
    libro = buscar(raiz, codigo)
    if libro is None:
        return False
    libro.disponibles += 1
    return True

def total_disponibles(nodo):
    if nodo is None:
        return 0
    return (nodo.disponibles
            + total_disponibles(nodo.izquierdo)
            + total_disponibles(nodo.derecho))

def bajo_inventario(nodo):
    if nodo is None:
        return []
    izquierda = bajo_inventario(nodo.izquierdo)
    actual = [nodo.codigo] if nodo.disponibles <= 1 else []
    derecha = bajo_inventario(nodo.derecho)
    return izquierda + actual + derecha


def procesar_movimientos(raiz, ruta):
    aceptados = rechazados = 0
    with open(ruta, encoding='utf-8') as archivo:
        for numero, linea in enumerate(archivo, 1):
            if not linea.strip():
                continue
            partes = linea.strip().split('|')
            if len(partes) != 2:
                raise ValueError(f'Línea {numero} incorrecta')
            codigo_texto, operacion = partes
            codigo = int(codigo_texto)
            if operacion == 'PRESTAMO':
                exito = prestar(raiz, codigo)
            elif operacion == 'DEVOLUCION':
                exito = devolver(raiz, codigo)
            else:
                raise ValueError(f'Operación inválida en línea {numero}')
            if exito:
                aceptados += 1
            else:
                rechazados += 1
    return aceptados, rechazados



print("-----------------------------------------------")
print("Primera seccion")
print("-----------------------------------------------")
print(prestar(raiz, 330))  # True: pasa de 2 a 1
print(prestar(raiz, 330))  # True: pasa de 1 a 0
print(prestar(raiz, 330))  # False: no hay ejemplares
print(prestar(raiz, 999))  # False: código inexistente
print(buscar(raiz, 330).disponibles)  # 0
print("\n")

print("-----------------------------------------------")
print("Segunda seccion")
print("-----------------------------------------------")
print(devolver(raiz, 580))  # True: pasa de 1 a 2
print(devolver(raiz, 999))  # False: catálogo sin cambios
print(buscar(raiz, 580).disponibles)  # 2
print("\n")

print("-----------------------------------------------")
print("Reporte Recursivo")
print("-----------------------------------------------")
print('Ejemplares disponibles:', total_disponibles(raiz))
print('Códigos de bajo inventario:', bajo_inventario(raiz))
print("\n")

print("-----------------------------------------------")
print("Insertar")
print("-----------------------------------------------")
raiz = insertar(raiz, 520, 'Seguridad informática', 2)
print([codigo for codigo, _, _ in listado_inorden(raiz)])
print(total_disponibles(raiz))
print("\n")

print("-----------------------------------------------")
print("Quinta seccion")
print("-----------------------------------------------")
try:
    raiz = insertar(raiz, 520, 'Seguridad informática', 2)
except ValueError as e:
    print(f'Error: {e}')
print([codigo for codigo, _, _ in listado_inorden(raiz)])
print(total_disponibles(raiz))
print("\n")

print("-----------------------------------------------")
print("Sexta seccion")
print("-----------------------------------------------")
raiz_lote = cargar_catalogo('catalogo_libros.txt')
aceptados, rechazados = procesar_movimientos(raiz_lote, 'movimientos.txt')
print('Aceptados:', aceptados, 'Rechazados:', rechazados)
print('Existencias:', total_disponibles(raiz_lote))
print('Bajo inventario:', bajo_inventario(raiz_lote))
print("\n")