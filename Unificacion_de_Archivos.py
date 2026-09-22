import csv
import unicodedata

class Nodo:
    def __init__(self, identificador, especie, pais, codigo):
        self.identificador = identificador
        self.especie = especie
        self.pais = pais
        self.codigo = codigo
        self.anterior = None
        self.siguiente = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.final = None
        self.cantidad = 0

    def agregar_final(self, identificador, especie, pais, codigo):
        nuevo = Nodo(identificador, especie, pais, codigo)
 
        if self.cabeza is None:
            self.cabeza = nuevo
            self.final = nuevo
        else:
            nuevo.anterior = self.final
            self.final.siguiente = nuevo
            self.final = nuevo
 
        self.cantidad += 1

    def mostrar_primeros(self, limite=5):
        actual = self.cabeza
        contador = 0
 
        while actual is not None and contador < limite:
            print(actual.identificador, actual.especie,
                  actual.pais, actual.codigo, sep=" | ")
            actual = actual.siguiente
            contador += 1
 
    def mostrar_atras(self, limite=5):
        actual = self.final
        contador = 0
 
        while actual is not None and contador < limite:
            print(actual.identificador, actual.especie,
                  actual.pais, actual.codigo, sep=" | ")
            actual = actual.anterior
            contador += 1

    def buscar_por_pais(self, pais_buscado):
        actual = self.cabeza
        encontrados = []
        pais_buscado = normalizar(pais_buscado)
 
        while actual is not None:
            if normalizar(actual.pais) == pais_buscado:
                encontrados.append(actual)
            actual = actual.siguiente
 
        return encontrados

    def guardar_archivo(self, nombre_archivo):
        actual = self.cabeza
 
        with open(nombre_archivo, "w", encoding="utf-8",
                  newline="") as archivo:
            escritor = csv.writer(archivo, delimiter=";")
            escritor.writerow([
                "ID", "Especie", "País", "Código_ISO_Alpha3"
            ])
 
            while actual is not None:
                escritor.writerow([
                    actual.identificador,
                    actual.especie,
                    actual.pais,
                    actual.codigo
                ])
                actual = actual.siguiente

def normalizar(texto):
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

def cargar_codigos(nombre_archivo):
    codigos = {}

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=";")
        next(lector)

        for fila in lector:
            if len(fila) == 2:
                pais = fila[0]
                codigo = fila[1]
                codigos[normalizar(pais)] = codigo

    return codigos

def cargar_arboles(nombre_archivo, codigos, lista):
    equivalencias = {
        "republica checa": "chequia",
        "estados unidos de america": "estados unidos",
        "nueva zelandia": "nueva zelanda",
        "republica de corea": "corea del sur",
        "federacion de rusia": "rusia",
        "myanmar": "myanmar (birmania)"
    }
    paises_no_encontrados = set()

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=";")
        next(lector)

        for fila in lector:
            if len(fila) == 3:
                identificador = int(fila[0])
                especie = fila[1]
                pais = fila[2]
                pais_normalizado = normalizar(pais)
                pais_normalizado = equivalencias.get(
                    pais_normalizado, pais_normalizado
                )
                codigo = codigos.get(
                    pais_normalizado, "NO_ENCONTRADO"
                )

                if codigo == "NO_ENCONTRADO":
                    paises_no_encontrados.add(pais)

                lista.agregar_final(
                    identificador, especie, pais, codigo
                )

    return paises_no_encontrados

def generar_reporte_centroamerica(lista, archivo_salida="reporte_centroamerica.txt", paises_objetivo=None):
    if paises_objetivo is None:
        paises_objetivo = ["Guatemala", "El Salvador", "Honduras", "Costa Rica"]

    mapa_paises = {}
    for p in paises_objetivo:
        norm = normalizar(p)
        mapa_paises[norm] = p
        if norm == "el salvador":
            mapa_paises["salvador"] = p

    datos = {p: set() for p in paises_objetivo}

    actual = lista.cabeza
    while actual is not None:
        pais_norm = normalizar(actual.pais)
        if pais_norm in mapa_paises:
            pais_oficial = mapa_paises[pais_norm]
            datos[pais_oficial].add(actual.especie)
        actual = actual.siguiente

    paises_ordenados = sorted(
        datos.items(),
        key=lambda item: len(item[1]),
        reverse=True
    )

    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        archivo.write("=" * 60 + "\n")
        archivo.write(" REPORTE DE ESPECIES DE ÁRBOLES - CENTROAMÉRICA\n")
        archivo.write("=" * 60 + "\n\n")

        for ranking, (pais, especies) in enumerate(paises_ordenados, start=1):
            archivo.write(f"{ranking}° {pais.upper()} ({len(especies)} especies registradas):\n")
            if especies:
                for especie in sorted(especies):
                    archivo.write(f"   • {especie}\n")
            else:
                archivo.write("   (No se encontraron especies registradas)\n")
            archivo.write("\n")

        archivo.write("=" * 60 + "\n")

    print(f"Reporte generado: {archivo_salida}")


def main():
    archivo_arboles = "especies_arboles_paises_1000.txt"
    archivo_codigos = "paises_codigos_iso_alpha3.txt"
    archivo_salida = "arboles_con_codigos_paises.txt"
    archivo_reporte = "reporte_centroamerica.txt"

    codigos = cargar_codigos(archivo_codigos)
    lista_arboles = ListaDoblementeEnlazada()
    no_encontrados = cargar_arboles(
        archivo_arboles, codigos, lista_arboles
    )
    lista_arboles.guardar_archivo(archivo_salida)

    print("Códigos cargados:", len(codigos))
    print("Registros almacenados:", lista_arboles.cantidad)

    if no_encontrados:
        print("Países sin código:", sorted(no_encontrados))
    else:
        print("Todos los países fueron relacionados correctamente.")

    print("Archivo generado:", archivo_salida)
    print("\nPrimeros cinco registros:")
    lista_arboles.mostrar_primeros(5)

    resultados = lista_arboles.buscar_por_pais("Costa Rica")
    print("\nÁrboles de Costa Rica encontrados:", len(resultados))

    generar_reporte_centroamerica(lista_arboles, archivo_reporte)


main()
