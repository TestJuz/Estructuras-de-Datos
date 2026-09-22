# Ejercicio programado: Árboles con archivos

Implementación en Python de los 4 subtipos de árboles vistos en el curso
de Estructuras de Datos, cada uno con soporte para **leer su estructura
desde un archivo** y **guardar (serializar) el árbol resultante en un
archivo**, pudiendo luego recargarlo.

## Contenido del proyecto

```
proyecto_arboles/
├── arbol_general.py      # 1. Árboles generales (N hijos por nodo)
├── arbol_binario.py      # 2. Árboles binarios (recorridos clásicos)
├── arbol_bst.py           # 3. Árboles binarios de búsqueda (BST)
├── arbol_avl.py            # 4. Árboles balanceados (AVL con rotaciones)
├── visualizador.py           # Genera diagramas .png y vista ASCII
├── main.py                  # Script de demostración de los 4 tipos
├── test_arboles.py          # 22 pruebas unitarias (casos límite incluidos)
├── requirements.txt          # Única dependencia opcional: matplotlib
├── datos/                    # Archivos de entrada de ejemplo
│   ├── general.txt
│   ├── binario.txt
│   ├── bst.txt
│   └── avl.txt
└── salida/                    # Aquí se generan los archivos guardados
    └── imagenes/                # y los diagramas .png de cada árbol
```

## Cómo ejecutar

```bash
# (Opcional, solo para las imágenes) instalar matplotlib:
pip install -r requirements.txt

# Demostración completa de los 4 tipos (lee de datos/, escribe en salida/)
python3 main.py

# Pruebas unitarias (no requieren librerías externas)
python3 test_arboles.py

# Cada módulo también se puede ejecutar solo, con un ejemplo embebido:
python3 arbol_general.py
python3 arbol_binario.py
python3 arbol_bst.py
python3 arbol_avl.py
```

El proyecto funciona completo con la biblioteca estándar de Python
únicamente. **La única dependencia externa es `matplotlib`**, y solo
se usa para generar las imágenes de los árboles (`visualizador.py`);
si no la instalás, `main.py` fallará solo en esa parte — podés
comentar esas líneas y el resto sigue funcionando igual.

## Ver los árboles de forma visual

Cada vez que corrés `main.py`, además de la salida en texto se genera:

1. **Una vista ASCII en la terminal** (sin necesitar matplotlib), por
   ejemplo:
   ```
   └── 8
       ├── 3
       │   ├── 1
       │   └── 6
       └── 10
           └── 14
   ```

2. **Una imagen `.png`** por cada árbol en `salida/imagenes/`, con los
   nodos como círculos/cajas y las conexiones dibujadas — el mismo
   estilo visual que las diapositivas del curso. El árbol AVL además
   muestra el **factor de balance** de cada nodo en rojo, para
   comprobar visualmente que ninguno excede ±1.

   Podés abrir esos `.png` directamente en VS Code (clic en el
   archivo en el explorador) para ver el árbol dibujado.


## Formatos de archivo utilizados

Cada tipo de árbol necesita un formato distinto porque su forma se
determina de manera diferente:

| Tipo | Formato de archivo | Ejemplo |
|---|---|---|
| **General** | Relaciones `padre,hijo` (una por línea); `ROOT,x` marca la raíz | `ROOT,A` / `A,B` |
| **Binario** | Recorrido **por niveles**, separado por comas; `-` = sin hijo | `8,3,10,1,6,-,14` |
| **BST** | Lista de valores a **insertar en orden** | `8,3,10,1,6,14` |
| **AVL** | Lista de valores a **insertar en orden** (se autobalancea) | `10,20,30,40,50` |

Al **guardar** un árbol binario, BST o AVL, siempre se usa el formato
"por niveles con `-`", porque es el único que preserva la **forma
exacta** del árbol (no solo sus valores). Si guardáramos solo los
valores en inorden y los reinsertáramos, perderíamos información sobre
el orden real de inserción o las rotaciones aplicadas.

## Qué demuestra cada módulo

### 1. `arbol_general.py`
- Construcción a partir de relaciones padre-hijo leídas de un archivo.
- Recorrido preorden, altura, conteo de nodos.
- Validación de errores: archivo mal formado o sin raíz lanza `ValueError`
  (buena práctica de seguridad al procesar archivos externos, tal como
  se explicó en la sección de seguridad de la presentación de Árboles).

### 2. `arbol_binario.py`
- Construcción desde el recorrido por niveles (algoritmo con cola/BFS).
- Los 4 recorridos clásicos: preorden, inorden, postorden y por niveles.
- `destruir()` implementa la liberación en **postorden** (hijos antes
  que el nodo), replicando la buena práctica de manejo de memoria
  explicada en clase, aunque Python libere memoria automáticamente.

### 3. `arbol_bst.py`
- Inserción, búsqueda y **eliminación con los 3 casos clásicos** (hoja,
  un hijo, dos hijos con sucesor).
- `es_valido_bst()` verifica la propiedad de orden recorriendo en
  inorden — útil para validar árboles cargados desde una fuente externa.
- Dos formas de cargar: `cargar_desde_archivo()` (reinserta valores,
  determinando la forma) y `cargar_forma_exacta_desde_archivo()`
  (reconstruye por niveles, preservando la forma guardada).

### 4. `arbol_avl.py`
- Inserción con **rebalanceo automático**: las 4 rotaciones (simple
  izquierda/derecha y dobles LR/RL) implementadas y probadas
  individualmente.
- `mostrar_factores_balance()` imprime cada nodo con su altura y su
  factor de balance, para verificar visualmente que ningún nodo excede
  ±1.
- `esta_balanceado()` es una verificación independiente del proceso de
  inserción (revisa TODOS los nodos), útil como prueba de corrección.

## Pruebas unitarias (`test_arboles.py`)

22 pruebas sin dependencias externas, incluyendo casos límite:

- Árboles vacíos y de un solo nodo.
- Los 3 casos de eliminación en BST (hoja, un hijo, dos hijos), incluida
  la eliminación de la raíz y de un valor inexistente.
- Las **4 rotaciones del AVL** (LL, RR, LR, RL) verificadas explícitamente
  comprobando qué nodo termina como raíz tras la rotación.
- Inserción de 100 valores ascendentes en un AVL, confirmando que la
  altura se mantiene cercana a log₂(n) en vez de degenerar a una lista.
- Round-trip completo (guardar → recargar) para los 4 tipos, verificando
  que la estructura se preserva exactamente.
- Manejo de archivos mal formados (deben lanzar `ValueError`, no fallar
  silenciosamente ni corromper el programa).

## Conexión con la teoría vista en clase

Este ejercicio integra conceptos de las 3 presentaciones del curso:

- **Árboles**: estructura de cada nodo, recorridos, complejidad,
  el caso degenerado de un BST y por qué el AVL lo resuelve.
- **Manejo de memoria y seguridad**: validación de archivos externos
  antes de confiar en ellos, patrón de liberación postorden, y por qué
  nunca se debe asumir que los datos de un archivo están bien formados.
- **Buenas prácticas de ingeniería**: separación en módulos, pruebas
  automatizadas, y verificación round-trip como forma de detectar
  errores de serialización.
