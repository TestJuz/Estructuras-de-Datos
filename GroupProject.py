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
        if self.IsEmpty():
            return
        current = self.head
        position = 0
        
        while current:
            if current.data == data:
                return position
            current = current.next
            position +=1
        return -1

    def EliminarAlFinal(self):
        if self.IsEmpty():
            return
        if self.tamanio <= 1:
            self.head = None
            self.tail = None
            return
        self.tail = self.tail.previous
        self.tail.next = None
        return
