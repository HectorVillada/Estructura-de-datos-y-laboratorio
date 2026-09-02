import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.RandomAccessFile;

public class MatrizDiscoStreaming {
    static final long N = 100000L;
    static final String ARCHIVO_NOMBRE = "matriz.dat";

    public static void main(String[] args) {
        try {
            long totalBytes = N * N;
            System.out.println("1. Creando archivo binario de 9.31 GB en disco...");
            
            try (RandomAccessFile file = new RandomAccessFile(ARCHIVO_NOMBRE, "rw")) {
                file.seek(0);
                file.writeByte(5);

                // Marca 1 al final de la primera fila (byte 99,999)
                file.seek(N - 1);
                file.writeByte(1);

                // Asignacion directa de tamaño
                file.seek(totalBytes - 1);
                file.writeByte(7);
            }

            System.out.println("2. Verificando matriz en disco por streaming (Conteo de 100,000 bytes/fila)...");
            try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream(ARCHIVO_NOMBRE), 64 * 1024)) {
                long contadorFila = 0;
                int numeroFila = 0;
                int byteLeido;

                while ((byteLeido = bis.read()) != -1 && numeroFila < 3) {
                    contadorFila++;
                    if (contadorFila == N) {
                        System.out.println("-> Fila " + numeroFila + " completada con " + contadorFila + " bytes. [Marca: " + byteLeido + "]");
                        contadorFila = 0;
                        numeroFila++;
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}