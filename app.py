class node:
    def __init__(self,data):
        self.data = data # Valor
        self.next = None # Puntero siguiente

#Fin de la clase nodo

#Creacion de la lista
class LinkedList:
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
            count=count+1 #Suma para saber la cantidad de datos que hay
        return count # Retorna el tamanio
        

    def AddinMiddle(self,data):
        current = self.head
        new_node = node(data)
         
        size = int(self.GetSize()/2) # la mitad relativa de la lista

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

        



        


lista1 = LinkedList()
lista1.insert(10)
lista1.insert(20)
lista1.insert(30)
lista1.insert(50)
lista1.insert(60)
print("Lista de 0 a 60 sin 40")
lista1.display() #muestra la lista
print("Insertar al frente")
lista1.AddInFront(0)
lista1.display() #muestra la lista
print("Insertar al Medio")
lista1.AddinMiddle(40)
lista1.display() #muestra la lista
print("eliminar el medio")
lista1.eliminarEnPosicion(3)
lista1.display() #muestra la lista
print("eliminar al head")
lista1.eliminarAlhead()
lista1.display() #muestra la lista
print("eliminar al final")
lista1.eliminarAlFinal()
lista1.display() #muestra la lista




