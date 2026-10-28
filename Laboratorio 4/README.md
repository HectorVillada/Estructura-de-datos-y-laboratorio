# Laboratorio 4: Sistema de Logística de Entregas - Árbol QuadTree en K-Dimensiones

Este proyecto consiste en la implementación desde cero de una estructura de datos espacial **QuadTree (Hyperquadtree en K-dimensiones)** en Python para optimizar las consultas de logística en una red urbana con 10.000 puntos estáticos de entrega.

---

## 📋 Declaración de Uso de IA Generativa e Integridad Académica

En cumplimiento del **Código de Honor** institucional y las directrices establecidas para el uso de herramientas tecnológicas en laboratorios:

1. **Uso de la IA:** Se utilizó Inteligencia Artificial Generativa (asistente de código) únicamente como herramienta de apoyo para:
   - Apoyo en la estructuración de la lógica matemática de la intersección entre un hipercubo (`BoundingBox`) y una hiperesfera (`query_range` y `nearest_neighbor`).
   - Apoyo en el diseño de las funciones de visualización gráfica en 2D con `matplotlib`.
   - Generación de la plantilla base de pruebas unitarias (`unittest`).

2. **Responsabilidad del Estudiante:** Todo el código fue revisado, refactorizado, probado y comprendido a plenitud por el estudiante. Nos hacemos totalmente responsables de la explicación técnica y matemática de cada elemento de esta entrega durante la sustentación.

---

## Estructura del Repositorio

```text
├── README.md               # Documentación general y declaración de honestidad
├── Quadtreetree.py         # Implementación desde cero del QuadTree/Hyperquadtree y Fuerza Bruta
├── test.py                 # Pruebas unitarias, verificación de consistencia y visualización 2D
└── analisis.py             # Benchmarking de rendimiento y gráficas comparativas
```

## Requisitos e Instalación

Para ejecutar las pruebas y generar las gráficas de rendimiento, solo se requieren las librerías estándar de Python y matplotlib:

```powershell
py -m pip install matplotlib
```

## Pruebas Unitarias y Visualización

Valida la exactitud del QuadTree comparando sus resultados con Fuerza Bruta y genera la imagen verificacion_quadtree.png:

```powershell
py test
```

## Análisis de Rendimiento (`analisis.py`)

Ejecuta la medición de tiempos para diferentes tamaños de datos $N$ ($10$ a $20.000$ puntos) y guarda la gráfica rendimiento_comparativo.png:

```powershell
py analisis.py
```

## Interpretación de los Resultados e Informe Comparativo

A partir de los experimentos ejecutados en `analisis.py`, se concluye lo siguiente:

1. **Punto de corte (*Crossover Point*):**

   - Con N = 10, Fuerza Bruta (alrededor de 0.0079 ms) y QuadTree (alrededor de 0.0082 ms) tardan prácticamente lo mismo debido al pequeño *overhead* inicial de la estructura en árbol.
   - A partir de aproximadamente 20 a 50 puntos, el QuadTree comienza a ser consistentemente más rápido que la Fuerza Bruta.

2. **Crecimiento de la Complejidad Algorítmica:**

   - **Fuerza Bruta, complejidad O(N):** El tiempo escala de forma lineal. Para 10.000 puntos, toma alrededor de 16.16 ms, y para 20.000 puntos sube linealmente a alrededor de 29.50 ms.
   - **QuadTree, complejidad aproximada O(log N) / O(k):** El tiempo crece de forma logarítmica o sublineal gracias a la poda de ramas. Para 10.000 puntos, la consulta toma solo alrededor de 0.45 ms (¡más de **35 veces más rápido** que Fuerza Bruta!).

3. **Conclusión para el Problema de Logística:**

   - Dado que el enunciado especifica **10.000 puntos de entrega estáticos**, construir el QuadTree una sola vez con una complejidad de O(N log N) justifica enormemente la inversión inicial, ya que cada consulta posterior de radio o vecino más cercano responderá en una fracción de milisegundo en tiempo real.

## Guía para la Sustentación

Puntos clave a presentar en la sustentación del Calendly:

1. **Estructura en K-Dimensiones:** Explicar cómo el árbol realiza divisiones en 2 elevado a K regiones utilizando máscaras de bits (`(i >> dim) & 1`) sobre el punto medio de cada eje.
2. **Poda de Ramas (*Pruning*):** Demostrar cómo `intersects_sphere` calcula la distancia mínima de un `BoundingBox` al centro de consulta para omitir cuadrantes completos sin recorrer sus nodos.
3. **Mapeo Espacial:** Confirmar que las coordenadas (x, y) representan unidades en metros, en un espacio de 10.000 m por 10.000 m, garantizando que el radio de 500 m responda con exactitud espacial.
