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

    def mostrar_productos_recursivo(self, nodo="__inicio__"):
        # Punto de entrada: primera llamada no pasa nodo, empieza en head
        if nodo == "__inicio__":
            if self.esta_vacia():
                print("No hay productos registrados.")
                return
            nodo = self.head

        # Caso base: llegamos al final de la lista
        if nodo is None:
            return

        print(nodo.producto)
        self.mostrar_productos_recursivo(nodo.next)

    def lista_doble_a_cola(self):
       
        cola = deque()
        actual = self.head

        while actual is not None:
            siguiente = actual.next  # guardamos antes de posiblemente desligar el nodo

            if actual.producto.existencias == 0:
                cola.append(actual.producto)
                self.eliminar_producto(actual.producto.id_producto)

            actual = siguiente

        return cola

    def generar_frecuencia_paises(self):
        
        frecuencias = {}
        actual = self.head

        while actual:
            pais = actual.producto.pais_origen
            frecuencias[pais] = frecuencias.get(pais, 0) + 1
            actual = actual.next

        return frecuencias

    def generar_reporte_recuperacion(self, ruta_archivo="archivo.txt"):
      
        if self.esta_vacia():
            return False, 0.0

        total_general = 0.0

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write("REPORTE DE RECUPERACION - SUPERMERCADO\n")
            archivo.write("=" * 60 + "\n\n")

            actual = self.head
            while actual:
                p = actual.producto
                subtotal = p.precio * p.existencias
                total_general += subtotal

                archivo.write(
                    f"ID: {p.id_producto} | Nombre: {p.nombre} | "
                    f"Precio: {p.precio:.2f} | Existencias: {p.existencias} | "
                    f"Subtotal: {subtotal:.2f}\n"
                )

                actual = actual.next

            archivo.write("\n" + "=" * 60 + "\n")
            archivo.write(f"TOTAL A RECUPERAR: {total_general:.2f}\n")

        return True, total_general


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
            cola = lista.lista_doble_a_cola()

            if cola:
                print("Productos sin existencias pasados a la cola (y eliminados de la lista):")
                for producto in cola:
                    print(producto)
            else:
                print("No hay productos sin existencias.")
        elif opcion == "5":
            frecuencias = lista.generar_frecuencia_paises()

            if not frecuencias:
                print("No hay productos registrados.")
            else:
                print("\nFrecuencia de productos por pais de origen:")
                # Ordenamos de mayor a menor frecuencia
                paises_ordenados = sorted(
                    frecuencias.items(), key=lambda item: item[1], reverse=True
                )

                for pais, cantidad in paises_ordenados:
                    print(f"{pais}: {cantidad} producto(s)")

                pais_top, cantidad_top = paises_ordenados[0]
                print(
                    f"\nEl pais desde el que mas se importa es: "
                    f"{pais_top} ({cantidad_top} producto(s))"
                )
        elif opcion == "6":
            exito, total = lista.generar_reporte_recuperacion("archivo.txt")

            if exito:
                print(f"Reporte generado en 'archivo.txt'. Total a recuperar: {total:.2f}")
            else:
                print("No hay productos registrados, no se genero el reporte.")
        elif opcion == "7":
            lista.mostrar_productos_recursivo()
        elif opcion == "8":
            print("Programa finalizado.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()