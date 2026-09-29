with open('catalogo_libros.txt', encoding='utf-8') as archivo:
    print('Primer libro:', archivo.readline().strip())
with open('movimientos.txt', encoding='utf-8') as archivo:
    print('Primer movimiento:', archivo.readline().strip())
