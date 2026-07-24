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
        


lista1 = LinkedList()
lista1.insert(10)
lista1.insert(20)
lista1.insert(30)
lista1.insert(40)
lista1.insert(50)
lista1.insert(60)
lista1.AddInFront(0)

lista1.display() #muestra la lista

