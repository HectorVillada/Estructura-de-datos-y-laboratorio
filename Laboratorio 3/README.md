# Laboratorio 3: Benchmark de estructuras de datos

## Descripción

Este proyecto compara el tiempo de búsqueda de tres estructuras que almacenan registros de estudiantes: una lista secuencial, un árbol binario de búsqueda (ABB) y un árbol B+. El benchmark ejecuta búsquedas con distintos tamaños de entrada y con identificadores insertados en orden aleatorio o ascendente. Los resultados se guardan en un CSV y se representan en seis gráficas.

El experimento principal está implementado en [laboratorio3.py](laboratorio3.py), y las gráficas se generan con [generar_graficas.py](generar_graficas.py). El archivo [b+ Arbol.py](b%2B%20Arbol.py) contiene, además, una demostración independiente de las estructuras y una medición sencilla.

## Archivos

- `laboratorio3.py`: estructuras de datos, generación de datos y benchmark adaptativo.
- `b+ Arbol.py`: implementación demostrativa independiente con sus propios datos y mediciones.
- `generar_graficas.py`: lectura del CSV y generación de las seis figuras.
- `resultados_mediciones.csv`: resultados del experimento principal, con 24 combinaciones y tres corridas por combinación.
- `fig1_tiempos_totales_cumplimiento.png` a `fig6_coeficiente_variacion.png`: gráficas generadas a partir del CSV.

## Funcionamiento del benchmark

### Datos y operaciones

En `laboratorio3.py`:

- `generar_datos(n)` crea `n` estudiantes con identificadores únicos y nombres seleccionados de una lista.
- `ListaEstudiantes.insertar(est)` agrega un registro al final de una lista. `buscar(id_est)` recorre los registros hasta encontrar el identificador o llegar al final. La búsqueda es $O(N)$.
- `NodoABB` guarda un estudiante y sus referencias izquierda y derecha. `ABB.insertar(est)` coloca cada registro según su ID, y `ABB.buscar(id_est)` sigue esas comparaciones hasta encontrarlo o alcanzar una rama vacía. En promedio, el ABB puede buscar en $O(\log N)$ con inserciones aleatorias; si recibe IDs ordenados, puede degenerar a $O(N)$.
- `NodoBPlus` representa un nodo del árbol B+ con claves, hijos y una referencia a la hoja siguiente. `ArbolBPlus.insertar(est)` inicia la inserción; `_insertar_no_lleno(nodo, clave, est)` encuentra el nodo donde corresponde insertar y mantiene las claves de las hojas ordenadas; `_dividir(padre, i, hijo)` separa un nodo lleno, actualiza las claves del padre y conserva los enlaces entre hojas. `buscar(id_est)` usa las claves internas para elegir una rama y busca la clave en la hoja correspondiente. Con orden 32, el recorrido entre niveles crece aproximadamente como $O(\log_{32} N)$.
- `medir_busquedas(estructura, ids_busqueda)` mide únicamente el lote de búsquedas mediante `time.perf_counter()`; no incluye la generación de datos ni la construcción de la estructura.
- `ejecutar_experimentos()` recorre tamaños, patrones y estructuras; ejecuta las repeticiones, calcula promedios y desviaciones, y escribe `resultados_mediciones.csv`.

### Diseño experimental

Se prueban los tamaños $N = 5{,}000$, $10{,}000$, $20{,}000$ y $40{,}000$, en dos modos: IDs aleatorios y IDs ordenados. Cada combinación de tamaño, modo y estructura se ejecuta tres veces ($R=3$), para un total de 24 filas de resultados.

El número de búsquedas $M$ se configura por estructura y modo para obtener mediciones suficientemente largas sin usar el mismo volumen de trabajo para algoritmos con costos muy distintos:

| Modo | Lista | ABB | Árbol B+ |
|---|---:|---:|---:|
| Aleatorios | 25,000 | 4,000,000 | 3,000,000 |
| Ordenados | 25,000 | 15,000 | 3,000,000 |

En cada lote, el 80% de las búsquedas usa IDs existentes y el 20% usa IDs inexistentes. Se seleccionan con reemplazo y se mezclan antes de medir.

Para comparar estructuras con diferentes valores de $M$, el CSV incluye el promedio por búsqueda en microsegundos:

$$\text{Promedio}_{\mu s/op} = \frac{\text{Tiempo total promedio (s)}}{M} \times 10^6$$

La desviación estándar por operación se calcula dividiendo la desviación estándar de los tiempos de corrida entre $M$ y multiplicando por $10^6$. Es una medida de variabilidad entre corridas, no un intervalo de confianza.

### Columnas del CSV

- `N`: número de estudiantes.
- `M`: número de búsquedas del lote.
- `Modo`: inserción aleatoria u ordenada.
- `Estructura`: Lista, ABB o B+.
- `Tiempo_Total_s`: promedio del tiempo total de búsqueda, en segundos.
- `Promedio_us_op`: tiempo promedio por búsqueda, en microsegundos.
- `Desviacion_us_op`: desviación estándar por búsqueda, en microsegundos.
- `Corridas`: número de repeticiones usadas para el promedio.

## Cómo interpretar las gráficas

Todas las figuras se generan a 300 DPI a partir de `resultados_mediciones.csv`.

1. **[Figura 1: tiempos totales](fig1_tiempos_totales_cumplimiento.png)**. Compara el tiempo total promedio según el tamaño, modo y estructura. El eje vertical es logarítmico; la línea horizontal en 1 segundo marca el umbral mínimo de medición indicado por la metodología.
2. **[Figura 2: eficiencia por búsqueda](fig2_eficiencia_unitaria_normalizada.png)**. Compara `Promedio_us_op` y muestra barras de error de una desviación estándar (`Desviacion_us_op`). La escala vertical logarítmica permite visualizar conjuntamente valores muy distintos.
3. **[Figura 3: ABB frente a B+ con IDs ordenados](fig3_abb_vs_bplus_ordenados.png)**. Muestra el costo por búsqueda al crecer $N$. Permite observar cómo el ABB se degrada cuando las inserciones ordenadas lo dejan desbalanceado, mientras el B+ conserva su estructura balanceada.
4. **[Figura 4: sensibilidad al patrón de entrada](fig4_sensibilidad_patron_entrada.png)**. Compara, para el mayor tamaño disponible, el tiempo por búsqueda con IDs aleatorios y ordenados. El eje vertical es logarítmico.
5. **[Figura 5: búsquedas frente a tiempo total](fig5_relacion_m_vs_tiempo_total.png)**. Relaciona el número de búsquedas $M$ asignado con el tiempo total medido. El eje horizontal es logarítmico; los símbolos identifican las estructuras.
6. **[Figura 6: variabilidad de las mediciones](fig6_coeficiente_variacion.png)**. Presenta el coeficiente de variación en porcentaje para las corridas con modo aleatorio: $CV\% = (\sigma/\mu) \times 100$. Un valor menor indica menor variabilidad relativa entre las corridas; no demuestra por sí solo que no exista ruido del sistema.

## El archivo `b+ Arbol.py`

Este archivo es una demostración separada del benchmark principal. `generar_estudiantes(n)` crea registros con ID, nombre y promedio; `N_ESTUDIANTES` y `N_BUSQUEDAS` fijan sus tamaños de demostración. La lista implementa inserción al final y búsqueda lineal. En el ABB, `_insertar_recursivo` coloca cada nodo y `_buscar_recursivo` busca por ID; como ambas funciones son recursivas, insertar IDs ordenados puede producir un árbol profundo y alcanzar el límite de recursión. En el B+, `_insertar_no_lleno` desciende hasta la hoja adecuada y `_dividir_hijo` parte los nodos llenos y actualiza el padre. `ejecutar_benchmark(datos, titulo)` construye las tres estructuras, elige 100 IDs existentes, mide sus búsquedas y muestra los tiempos. El bloque principal genera y ejecuta los casos aleatorio y ordenado. Sus mediciones usan `time.time()` y no se exportan al CSV ni alimentan las seis gráficas.

## Ejecución

Se requiere Python 3.8 o superior, además de `pandas` y `matplotlib` para crear las figuras. En PowerShell:

```powershell
py -m pip install pandas matplotlib
py laboratorio3.py
py generar_graficas.py
```

`laboratorio3.py` tarda varios minutos porque ejecuta millones de búsquedas en algunas combinaciones y reemplaza `resultados_mediciones.csv` al terminar. `generar_graficas.py` usa ese CSV y guarda las seis imágenes en la carpeta actual. Para ejecutar la demostración independiente:

```powershell
py "b+ Arbol.py"
```

## Uso de inteligencia artificial y código de honor

Se utilizó **Gemini**, modelo de inteligencia artificial de Google, como herramienta de apoyo durante el desarrollo del trabajo. La asistencia se empleó en la conceptualización del número adaptativo de búsquedas $M$ y la normalización del tiempo por operación, en el apoyo al tratamiento y presentación gráfica de los resultados, y en la organización y explicación de la documentación. La redacción y revisión de este README también contó con apoyo de **GitHub Copilot**.

El uso de IA se declara de forma transparente y no sustituye la responsabilidad académica del estudiante. El estudiante declara haber revisado y verificado las implementaciones y los resultados en su entorno, y conserva la responsabilidad de comprender el código, ejecutar las pruebas y sustentar las decisiones tomadas, de acuerdo con el código de honor de la asignatura.

## Alcance

La versión actual del repositorio contiene el benchmark y la generación de gráficas descritos arriba. Aunque una versión previa de esta documentación mencionaba un módulo de Árbol de Merkle, en los archivos actuales no existe `merkle_tree.py` ni una implementación de verificación criptográfica; por eso no se documenta como funcionalidad disponible.


