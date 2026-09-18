import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.RandomAccessFile;

/**
 * Laboratorio 1 - Manejo de Grandes Volúmenes de Datos en Disco
 * 
 * Este programa resuelve la manipulación de una matriz de 100,000 x 100,000 elementos
 * (10,000,000,000 bytes = ~9.31 GB) optimizando:
 * 1. Consumo de RAM: Uso nulo de RAM mediante el uso de disco como soporte físico.
 * 2. Escritura rápida: Mapeo de archivos dispersos (Sparse Files) vía RandomAccessFile.
 * 3. Lectura eficiente: Procesamiento por bloques mediante BufferedInputStream (Streaming).
 */
public class MatrizDiscoStreaming {

    // Tamaño de la matriz: 100,000 x 100,000 (10^10 bytes = ~9.31 GB)
    static final long N = 100_000L;
    static final String ARCHIVO_NOMBRE = "matriz.dat";

    public static void main(String[] args) {
        try {
            long totalBytes = N * N;

            // =========================================================================
            // FASE 1: CREACIÓN Y ESCRITURA OPTIMIZADA EN DISCO (O(1) de RAM)
            // =========================================================================
            System.out.println("1. Creando archivo binario de " + (totalBytes / (1024 * 1024 * 1024.0)) + " GB...");
            long inicioCreacion = System.currentTimeMillis();

            try (RandomAccessFile file = new RandomAccessFile(ARCHIVO_NOMBRE, "rw")) {
                // Escribir un valor arbitrario en el origen (0,0)
                file.seek(0);
                file.writeByte(5);

                // Marcar el fin de la primera fila (columna 99,999) con un delimitador '1'
                file.seek(N - 1);
                file.writeByte(1);

                // Marcar una celda central
                long posCentro = 50_000L * N + 50_000L;
                file.seek(posCentro);
                file.writeByte(9);

                // Reservar y fijar el tamaño final del archivo (9.31 GB) de forma instantánea
                file.seek(totalBytes - 1);
                file.writeByte(7);
            }

            long finCreacion = System.currentTimeMillis();
            System.out.println("   -> Archivo creado exitosamente en " + (finCreacion - inicioCreacion) + " ms.\n");

            // =========================================================================
            // FASE 2: VERIFICACIÓN Y LECTURA MEDIANTE STREAMING POR BLOQUES
            // =========================================================================
            System.out.println("2. Verificando contenido del archivo mediante Streaming...");
            
            // Usamos un buffer de 64 KB para no saturar RAM y leer secuencial a alta velocidad
            int bufferSize = 64 * 1024; 
            try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream(ARCHIVO_NOMBRE), bufferSize)) {
                
                long contadorBytesFila = 0;
                long totalBytesProcesados = 0;
                int numeroFila = 0;
                int byteLeido;
                
                // Leemos únicamente las primeras 3 filas para la verificación en consola
                int filasALeer = 3;

                System.out.println("--- Inspección de Filas (Visualización de conteo de 100,000 bytes/fila) ---");

                while ((byteLeido = bis.read()) != -1 && numeroFila < filasALeer) {
                    contadorBytesFila++;
                    totalBytesProcesados++;

                    // Muestra los primeros 5 elementos visuales de la fila
                    if (contadorBytesFila <= 5) {
                        System.out.print(byteLeido + " ");
                    } else if (contadorBytesFila == 6) {
                        System.out.print("... ");
                    }

                    // Detección de salto de línea (Marca '1' o llegar al byte 100,000)
                    if (contadorBytesFila == N) {
                        System.out.println("-> [Marca/Byte final: " + byteLeido + "] " +
                                           "(Fin Fila " + numeroFila + " | Total conteo: " + contadorBytesFila + " bytes)");
                        contadorBytesFila = 0;
                        numeroFila++;
                    }
                }
            }

            // =========================================================================
            // FASE 3: CONSULTA DIRECTA (ACCESO ALEATORIO O(1))
            // =========================================================================
            System.out.println("\n3. Verificación puntual de coordenadas específicas en disco:");
            try (RandomAccessFile file = new RandomAccessFile(ARCHIVO_NOMBRE, "r")) {
                System.out.println("   - Valor en Celda (0, 0): " + leerCelda(file, 0, 0));
                System.out.println("   - Valor en Celda (0, 99999) [Fin Fila 0]: " + leerCelda(file, 0, 99999));
                System.out.println("   - Valor en Celda (50000, 50000) [Centro]: " + leerCelda(file, 50000, 50000));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Realiza un salto directo en el archivo mediante Row-Major Order.
     * Ubicación = (fila * N) + columna.
     */
    private static byte leerCelda(RandomAccessFile file, long fila, long col) throws Exception {
        long offset = fila * N + col;
        file.seek(offset);
        return file.readByte();
    }
}