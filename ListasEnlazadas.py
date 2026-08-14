class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamanio = 0

    def estaVacia(self):
        return self.cabeza is None

    def AgregarAlInicio(self,valor):
        nuevo_nodo = Nodo(valor)
        if self.estaVacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.tamanio += 1

    def RecorrerAdelante(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.valor, end="  ")
            actual = actual.siguiente
        print()

    def RecorrerAtras(self):
        actual = self.cola
        while actual is not None:
            print(actual.valor, end="  ")
            actual = actual.anterior
    def Buscar(self,valor):
        actual = self.cabeza
        posicion = 0
        while actual:
            if actual.valor == valor:
                return posicion
            actual = actual.siguiente
            posicion += 1
        return -1 # este elemento nunca estuvo en la lista doblemente enlazada

    def tamanio_lista(self):
        return self.tamanio

    def EliminarAlFinal(self):
        if self.estaVacia():
            print("La lista está vacía. No se puede eliminar ningún elemento.")
            return None
        valor_eliminado = self.cola.valor
        if self.cabeza == self.cola:  # Solo hay un nodo en la lista
            self.cabeza = None
            self.cola = None
        else:
            self.cola = self.cola.anterior
            self.cola.siguiente = None
        self.tamanio -= 1
        return valor_eliminado

    def insertar_final(self,valor):
        nuevo_nodo = Nodo (valor)
        if self.estaVacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamanio += 1 

    def insertar_medio(self,valor,posicion):
        if posicion < 0 or posicion > self.tamanio:
         print("Posicion Invalida.")
         return 

        if posicion == 0:
            self.AgregarAlInicio(valor)
            return  

        if posicion == self.tamanio:
            self.insertar_final(valor)
            return

        nuevo_nodo = Nodo(valor)

        actual = self.cabeza

        for i in range(posicion ):
            actual = actual.siguiente

        anterior = actual.anterior

        nuevo_nodo.anterior = anterior
        nuevo_nodo.siguiente = actual

        anterior.siguiente = nuevo_nodo
        actual.anterior = nuevo_nodo

        self.tamanio +=1

    def eliminar_inicio(self):
        if self.estaVacia():
            print("No existe algun elemento al cual eliminar")
            return None

        valor_eliminado = self.cabeza.valor
        if self.cabeza == self.cola:
            self.cabeza = None
            self.cola = None
        else:
            self.cabeza = self.cabeza.siguiente
            self.cabeza.anterior = None

        self.tamanio -=1

        return valor_eliminado

    def eliminarMedio(self,posicion):
        if self.estaVacia():
            print("No existe algun elemento al cual eliminar")
            return None

        if posicion < 0 or posicion >= self.tamanio:
            print ("Posicion Invalida.")
            return None

        if posicion == 0:
            return self.eliminar_inicio()

        if posicion == self.tamanio - 1:
            return self.EliminarAlFinal()

        actual = self.cabeza

        for i in range(posicion):
            actual = actual.siguiente

        valor_eliminado = actual.valor
        anterior = actual.anterior
        siguiente = actual.siguiente

        anterior.siguiente = siguiente
        siguiente.anterior = anterior 

        self.tamanio -= 1

        return valor_eliminado

    def encontrarPromedio(self):
        actual = self.cabeza
        valor = 0
        while actual is not None:
            valor += int(actual.valor)
            actual = actual.siguiente
        return float(valor/self.tamanio)
    
    def temperaturaMayor(self):
        if self.estaVacia():
            print("La Lista se encuentra vacia.")
            return None
        ppio = self.cabeza
        self.mayor = ppio.valor
        while ppio is not None:
            if ppio.valor > self.mayor:
                self.mayor = ppio.valor
            ppio = ppio.siguiente
        return self.mayor

    def temperaturaMenor(self):
        if self.estaVacia():
            print("La Lista se encuentra vacia.")
            return None
        ppio = self.cabeza
        self.menor = ppio.valor
        while ppio is not None:
            if ppio.valor < self.menor:
                self.menor = ppio.valor
            ppio = ppio.siguiente
        return self.menor




if __name__ == "__main__":
# Crear la lista doblemente enlazada
    lista = ListaDoblementeEnlazada()
    try:
        with open("datos.txt", "r") as archivo:
            for linea in archivo:
                linea = linea.strip() 
                # Evitar líneas vacías
                if linea != "":
                    valor = int(linea)
                    # Insertar el valor en la lista
                    lista.AgregarAlInicio(valor)
                    lista.RecorrerAdelante()
                    print(f"Cantidad de elementos: {lista.tamanio_lista()}")

    except FileNotFoundError:
        print("Error: el archivo datos.txt no existe.")
        exit()

    except ValueError:
        print("Error: el archivo contiene un dato que no es entero.")
        exit()

    with open("Reporte.txt", "w") as archivo:
        archivo.write("====================================\n")
        archivo.write("    REPORTE DE TEMPERATURAS\n")
        archivo.write("====================================\n\n")
        archivo.write(
            "Cantidad de temperaturas: "
            + str(lista.tamanio_lista())
            + "\n"
            + "Temperatura mayor: "
            + str(lista.temperaturaMayor())
            + "Temperatura menor: "
            + str(lista.temperaturaMenor())
            + "Temperatura promedio: "
            + str(lista.encontrarPromedio())
        )
      




#if __name__ == "__main__":
#   listaD = ListaDoblementeEnlazada()
#
#  



#   listaD.insertar_final(20)
#   listaD.insertar_medio(25,1)
#   listaD.insertar_final(15)
#   listaD.RecorrerAdelante()
#   print("Ahora usando los metodos de eliminar: ")

#  listaD.eliminarMedio(1)
# listaD.RecorrerAdelante()

#   listaD.eliminar_inicio()
#   listaD.RecorrerAdelante()

