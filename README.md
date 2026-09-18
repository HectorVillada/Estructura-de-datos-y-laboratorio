# Estructura de Datos y Laboratorios

Repositorio para la entrega y documentación de los laboratorios del curso de Estructura de Datos.
---
## Laboratorio 1: Matriz Masiva en Disco

**Estudiante:** Tu Nombre Completo

### Archivos
* `MatrizDiscoStreaming.java`: C�digo que crea y verifica la matriz de 100,000x100,000 celdas en disco.
* `README.md`: Documentaci�n de la soluci�n.

### Soluci�n a los Problemas
1. **RAM:** El archivo se procesa en disco con acceso aleatorio y streaming por bloques (buffer de 64 KB).
2. **Escritura Lenta:** Uso de Sparse Files v�a RandomAccessFile (`seek`) para asignaci�n instant�nea en $O(1)$.
3. **Verificaci�n:** Conteo secuencial que valida f�sicamente bloques de 100,000 bytes por fila junto con marcas delimitadoras.
---
## Laboratorio 2: Árbol de Merkle

Implementación completa de una estructura de Árbol de Merkle en Python (`merkle_tree.py`) para simular la verificación criptográfica de integridad y pruebas de inclusión en transacciones.

### Características e Implementación
* **Algoritmo de Hash**: Generación de resúmenes mediante SHA-256 (`hashlib`).
* **Manejo de niveles impares**: Duplicación automática del último nodo para el emparejamiento bottom-up.
* **Demostración de Inmutabilidad**: Evidencia del efecto avalancha al modificar una transacción.
* **Pruebas de Inclusión (Merkle Proof)**: Verificación en tiempo $O(\log N)$ mediante el cálculo del camino de hashes hermanos (posiciones `'L'` / `'R'`).

### Estructura de la Carpeta `Laboratorio 2 Arbol de Merkle`
* Contiene el código fuente script en Python con menú interactivo y la simulación del experimento de 5 transacciones.