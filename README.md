# Laboratorio 1: Matriz Masiva en Disco

**Estudiante:** Tu Nombre Completo

## Archivos
* `MatrizDiscoStreaming.java`: Código que crea y verifica la matriz de 100,000x100,000 celdas en disco.
* `README.md`: Documentación de la solución.

## Solución a los Problemas
1. **RAM:** El archivo se procesa en disco con acceso aleatorio y streaming por bloques (buffer de 64 KB).
2. **Escritura Lenta:** Uso de Sparse Files vía RandomAccessFile (`seek`) para asignación instantánea en $O(1)$.
3. **Verificación:** Conteo secuencial que valida físicamente bloques de 100,000 bytes por fila junto con marcas delimitadoras.
