from collections import deque


class Producto:
    def __init__(self, id_producto, nombre, precio, pais_origen, existencias):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.pais_origen = pais_origen
        self.existencias = existencias

    def __str__(self):
        return (
            f"ID: {self.id_producto} | "
            f"Nombre: {self.nombre} | "
            f"Precio: {self.precio:.2f} | "
            f"Pais de origen: {self.pais_origen} | "
            f"Existencias: {self.existencias}"
        )


class Nodo:
    def __init__(self, producto):
        self.producto = producto
        self.next = None
        self.previous = None


class ListaDobleProductos:
    def __init__(self):
        self.head = None
        self.tail = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.head is None

    def buscar_producto(self, id_producto):
        actual = self.head

        while actual:
            if actual.producto.id_producto == id_producto:
                return actual
            actual = actual.next

        return None

    def ingresar_producto(self, producto):
        if self.buscar_producto(producto.id_producto):
            return False

        new_node = Nodo(producto)

        if self.esta_vacia():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.tamanio += 1
        return True

    def eliminar_producto(self, id_producto):
        nodo = self.buscar_producto(id_producto)

        if not nodo:
            return False

        if nodo.previous:
            nodo.previous.next = nodo.next
        else:
            self.head = nodo.next

        if nodo.next:
            nodo.next.previous = nodo.previous
        else:
            self.tail = nodo.previous

        self.tamanio -= 1
        return True

    def mostrar_productos(self):
        if self.esta_vacia():
            print("No hay productos registrados.")
            return

        actual = self.head

        while actual:
            print(actual.producto)
            actual = actual.next

    def lista_doble_a_cola(lista_doble):
        cola = deque()
        actual = lista_doble.head
        while actual is not None:
            if actual.producto.existencias == 0:
                cola.append(actual.producto)
            actual = actual.next
        return cola 




def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()

        if valor:
            return valor

        print("El valor no puede estar vacio.")


def leer_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))

            if valor >= 0:
                return valor

            print("El valor debe ser mayor o igual a cero.")
        except ValueError:
            print("Ingrese un numero valido.")


def leer_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))

            if valor >= 0:
                return valor

            print("El valor debe ser mayor o igual a cero.")
        except ValueError:
            print("Ingrese un numero entero valido.")


def crear_producto():
    id_producto = leer_texto("ID del producto: ")
    nombre = leer_texto("Nombre del producto: ")
    precio = leer_float("Precio: ")
    pais_origen = leer_texto("Pais de origen: ")
    existencias = leer_entero("Existencias: ")

    return Producto(id_producto, nombre, precio, pais_origen, existencias)


def mostrar_menu():
    print("\nMenu de productos")
    print("1. Ingresar producto")
    print("2. Eliminar producto")
    print("3. Buscar producto")
    print("4. Pasar productos sin existencias a cola")
    print("5. Generar lista de frecuencias por pais")
    print("6. Generar reporte archivo.txt")
    print("7. Mostrar lista doblemente enlazada de forma recursiva")
    print("8. Salir")


def main():
    lista = ListaDobleProductos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            producto = crear_producto()

            if lista.ingresar_producto(producto):
                print("Producto ingresado correctamente.")
            else:
                print("Ya existe un producto con ese ID.")
        elif opcion == "2":
            id_producto = leer_texto("ID del producto a eliminar: ")

            if lista.eliminar_producto(id_producto):
                print("Producto eliminado correctamente.")
            else:
                print("No se encontro un producto con ese ID.")
        elif opcion == "3":
            id_producto = leer_texto("ID del producto a buscar: ")
            nodo = lista.buscar_producto(id_producto)

            if nodo:
                print(nodo.producto)
            else:
                print("No se encontro un producto con ese ID.")
        elif opcion == "4":
            cola = ListaDobleProductos.lista_doble_a_cola(lista)
            if cola:
                print("Productos sin existencias pasados a la cola:")
                for producto in cola:
                    print(producto)
            else:
                print("No hay productos sin existencias.")
        elif opcion == "5":
            print("Opcion pendiente de implementar.")
        elif opcion == "6":
            print("Opcion pendiente de implementar.")
        elif opcion == "7":
            print("Opcion pendiente de implementar.")
        elif opcion == "8":
            print("Programa finalizado.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()


