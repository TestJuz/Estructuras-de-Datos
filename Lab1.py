import os
class node:
    def __init__(self,data):
        self.data = data # Valor
        self.next = None # Puntero siguiente

#Fin de la clase nodo

#Creacion de la lista
class SimpleList:
    def __init__(self):
        self.head = None

    def insert(self,data):
        new_node = node(data)
        if(self.head is None):
            self.head = new_node
            return 
        current = self.head #Valor temporal para recorrer la lista 
        while(current.next):
            current = current.next #Recorre la lista hasta el final
        current.next = new_node #Lo guarda al final

    def display(self): #Se asemeja a un toString
        current = self.head
        while(current): #Recorre los nodos
            print(current.data, end=" -> ")
            current = current.next #Navegacion entre nodos 
        print("None")

    # Método público que inicia la recursión desde la cabeza (head)
    def displayRecursivo(self):
        self._display_interno(self.head)

    # Método privado que realiza la recursión nodo por nodo
    def _display_interno(self, actual):
        if actual is None:
            return
        
        print(actual.data)
        self._display_interno(actual.next)



    def AddInFront(self,data):
        new_node = node(data)
        if(self.head is None):
            self.head = new_node
            return 
        current = self.head #Toma el primero backup
        self.head = node(data) # Cambia el valor primero al nuevo
        self.head.next = current

    def GetSize(self):
        current = self.head
        count = int(0)
        while(current): #Recorre los nodos
            current = current.next #Navegacion entre nodos 
            count+=count #Suma para saber la cantidad de datos que hay
        return count # Retorna el tamanio
        

    def AddinMiddle(self,data):
        current = self.head
        new_node = node(data)
         
        size = int(self.GetSize()/2-1) # la mitad relativa de la lista

        while(size > 0): #Recorre los nodos hasta el medio
            current = current.next
            size = size -1 

        new_node.next = current.next # El nuevo nodo ahora tiene el valor siguiente que tenia el viejo medio
        current.next = new_node # El viejo medio ahora apunta al nuevo medio

    def eliminarEnPosicion(self,posicion):
        # Lista vacía
        if self.head is None:
            print("La lista está vacía.")
            return
        # Eliminar el primer nodo
        if posicion == 0:
            self.head = self.head.next
            return
        actual = self.head
        contador = 0
        # Buscar el nodo anterior a la posición
        while actual.next is not None and contador < posicion - 1:
            actual = actual.next
            contador += 1
        # Verificar si la posición existe
        if actual.next is None:
            print("Posición fuera de rango.")
            return
        # Saltar el nodo que se desea eliminar
        actual.next = actual.next.next
    
    def eliminarAlhead(self):
        if self.head is None:
            print("La lista está vacía.")
            return
        actual = self.head
        self.head = actual.next

    def eliminarAlFinal(self):

        if self.head is None:
            print("La lista está vacía.")
            return

        if self.head.next is None:
            self.head = None
            return

        actual = self.head

        while actual.next.next is not None:
            actual = actual.next

        actual.next = None

    def DeterminarVacio(self):  
        if self.head is None:
                print("La lista está vacía.")
                return  
        
        print("La lista no esta vacia")
        return

    def BuscarElemento(self,data):
        current = self.head
        contador = 0
        while( current): #Recorre los nodos hasta el medio
            if(current.data == data):
                print("encontrado en posicion: " + str(contador))
                return
            current = current.next
            contador = contador + 1
        
        print("elemento no encontrado")
        return






        


lista1 = SimpleList()

lista1.AddInFront(1)
lista1.AddInFront(2)
lista1.AddInFront(3)
lista1.AddInFront(4)
lista1.AddInFront(5)

lista1.displayRecursivo()
input("Presione una tecla para continuar")
opcion = 0

while(opcion != 9): 

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print("----------------------------------")
    print("Ingrese una opcion")
    print("0- Determinar si lista esta vacia")
    print("1- Imprimir lista")
    print("2- Insertar un numero al inicio")
    print("3- Insertar un numero al medio")
    print("4- Insertar un numero al final")
    print("5- Eliminar numero al inicio")
    print("6- Eliminar numero el numero en una posicion")
    print("7- Eliminar numero al final")
    print("8- Buscar en lista")
    print("9- Salir")
    print("----------------------------------")


    opcion = input("Ingrese una opcion: ")
    try:
        opcion = int(opcion)
    except ValueError:
        opcion = int(10)

    match opcion:
        case 0:
            lista1.DeterminarVacio()
            input("Presione una tecla para continuar")
        case 1:
            lista1.display()
            input("Presione una tecla para continuar")
        case 2:
            Addopcion = input("Ingrese el numero a insertar: ")
            try:
                Addopcion = int(Addopcion)
                lista1.AddInFront(int(Addopcion))
                lista1.display()
                input("Presione una tecla para continuar")
            except ValueError:
                input("Ingrese un numero")
    
        case 3:
            try:
                Addopcion = int(input("Ingrese el numero a insertar: "))
                lista1.AddinMiddle(int(Addopcion))
                lista1.display()
                input("Presione una tecla para continuar")
            except ValueError:
                input("Ingrese un numero")
        case 4:
            try:
                Addopcion = int(input("Ingrese el numero a insertar: "))
                lista1.insert(Addopcion)
                lista1.display()
                input("Presione una tecla para continuar")
            except ValueError:
                input("Ingrese un numero")
        case 5: 
            lista1.eliminarAlhead()
            lista1.display()
            input("Presione una tecla para continuar")
        case 6:
            try:
                lista1.display()
                Addopcion = int(input("Ingrese la posicion a eliminar: "))
                lista1.eliminarEnPosicion(Addopcion)
                lista1.display()
                input("Presione una tecla para continuar")
            except ValueError:
                input("Ingrese un numero")
        case 7:
            lista1.eliminarAlFinal()
            lista1.display()
            input("Presione una tecla para continuar")
        case 8:
            try:
                Addopcion = int(input("Ingrese un numero para buscar: "))
                lista1.display()
                lista1.BuscarElemento(Addopcion)
                input("Presione una tecla para continuar")
            except ValueError:
                input("Ingrese un numero")
        case 9: 
            print("Saliendo...")
            exit
        case _:
            print("Opcion no valida")
            input("Presione una tecla para continuar")

            


