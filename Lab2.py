import os
class node:
    def __init__(self,data):
        self.data = data # Valor
        self.next = None # Puntero siguiente
        self.previous = None # Puntero anterior

#Fin de la clase nodo

#Creacion de la lista
class LinkedList:
    def __init__(self):
        self.head = None #Inicio de la lista
        self.tail = None #Final de la lista
        self.tamanio = 0 #Tamaño de la lista

    def IsEmpty(self):
        return self.head is None

    def agregar_inicio(self, data):
        new_node = node(data)
        if self.IsEmpty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        self.tamanio += 1

    def Agregar_final(self,data):
        new_node = node(data)
        if self.IsEmpty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.previous = self.tail 
            self.tail.next = new_node
            self.tail = new_node
        self.tamanio +=1

    def recorrer_adelante(self):
        current = self.head
        while current:#actual == true
            print(current.data, end=" ")
            current = current.next
        print()


    def recorrer_atras(self):
        current = self.tail
        while current:#actual == true
            print(current.data, end=" ")
            current = current.previous
        print("None")

    def Buscar(self,data):
        current = self.head
        position = 0
        while current:
            if current.data == data:
                return position
            current = current.next
            position +=1
        return -1




            


       
        

        




lista1 = LinkedList()
lista1.Agregar_final(1)
lista1.Agregar_final(2)
lista1.Agregar_final(3)
lista1.Agregar_final(4)
lista1.recorrer_atras()

result = lista1.Buscar(2)
print("Elemento no encontrado" if result == -1 else "Elemento encontrado en la posición: " + str(result))