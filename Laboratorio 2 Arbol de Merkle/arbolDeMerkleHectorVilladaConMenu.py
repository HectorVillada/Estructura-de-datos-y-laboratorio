import hashlib

def get_hash(text: str) -> str:
    """
    Calcula el hash SHA-256 completo de una cadena de texto.
    1. Codifica el texto a formato de bytes en UTF-8.
    2. Aplica el algoritmo SHA-256 de la librería hashlib.
    3. Retorna la representación hexadecimal de 64 caracteres.
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def generar_transacciones_base():
    """
    Crea y retorna un banco estático de 20 transacciones simuladas
    para ser utilizadas en las pruebas del Árbol de Merkle.
    """
    return [
        "T1: Ana paga 150",   "T2: Luis paga 230",  "T3: Carlos paga 80", "T4: Maria paga 95",
        "T5: Pedro paga 40",  "T6: Lucia paga 60",  "T7: Sofia paga 120", "T8: Juan paga 30",
        "T9: Mateo paga 200", "T10: Elena paga 15", "T11: Diego paga 90", "T12: Nora paga 110",
        "T13: Raul paga 45",  "T14: Olga paga 75",  "T15: Ivan paga 300", "T16: Rosa paga 50",
        "T17: Hugo paga 180", "T18: Ines paga 220", "T19: Omar paga 130", "T20: Sara paga 99"
    ]

def obtener_niveles_arbol(transacciones: list) -> list:
    """
    Construye la estructura completa del Árbol de Merkle desde la base (hojas)
    hasta la cúspide (raíz), procesando nivel por nivel.
    
    Retorna una lista donde cada elemento es la lista de hashes de dicho nivel.
    """
    if not transacciones:
        return []

    # NIVEL 0 (Hojas): Hash SHA-256 individual de cada transacción base
    nivel_hojas = [get_hash(tx) for tx in transacciones]
    niveles = [nivel_hojas]

    # Iteración ascendente: continuar mientras el nivel superior tenga más de 1 nodo (raíz)
    while len(niveles[-1]) > 1:
        nivel_actual = niveles[-1].copy()
        
        # REGLA DEL ÁRBOL MERKLE: Si el número de nodos es impar, el último nodo se duplica
        if len(nivel_actual) % 2 != 0:
            nivel_actual.append(nivel_actual[-1])

        siguiente_nivel = []
        # Agrupar nodos en pares de dos (hermano izquierdo y hermano derecho)
        for i in range(0, len(nivel_actual), 2):
            nodo_izquierdo = nivel_actual[i]
            nodo_derecho = nivel_actual[i + 1]
            
            # El nodo padre almacena el hash de la concatenación de sus dos hijos
            hash_padre = get_hash(nodo_izquierdo + nodo_derecho)
            siguiente_nivel.append(hash_padre)

        # Se agrega la nueva capa calculada
        niveles.append(siguiente_nivel)

    return niveles

def generar_prueba_inclusion(index: int, niveles: list) -> list:
    """
    Genera la ruta o 'Prueba de Merkle' para una transacción dada su posición (index).
    
    Extrae únicamente los hashes 'hermanos' necesarios en cada nivel para poder
    reconstruir el camino matemático hasta la Merkle Root sin revelar el resto del árbol.
    """
    prueba = []
    # Recorrer todos los niveles salvo la raíz (último nivel)
    for nivel in niveles[:-1]:
        nivel_temp = nivel.copy()
        # Manejar caso de duplicación si la capa tiene número impar de elementos
        if len(nivel_temp) % 2 != 0:
            nivel_temp.append(nivel_temp[-1])

        # Determinar posición relativa (índices pares son hijos izquierdos)
        es_hijo_izquierdo = (index % 2 == 0)
        
        # Si es izquierdo, su hermano está a la derecha (+1). Si es derecho, a la izquierda (-1)
        idx_hermano = index + 1 if es_hijo_izquierdo else index - 1
        posicion_hermano = 'R' if es_hijo_izquierdo else 'L'

        # Se almacena la tupla: (Hash del hermano, Posición 'L' o 'R')
        prueba.append((nivel_temp[idx_hermano], posicion_hermano))
        
        # Dividir el índice entre 2 para posicionarse en el nodo padre del siguiente nivel
        index //= 2

    return prueba

def verificar_prueba_inclusion(tx: str, prueba: list, merkle_root: str) -> bool:
    """
    Verifica criptográficamente la validez de una prueba de inclusión.
    Calcula de abajo hacia arriba el hash resultante y lo compara contra la Merkle Root original.
    """
    # 1. Calcular hash base de la transacción a validar
    hash_actual = get_hash(tx)
    
    # 2. Reconstruir el camino de hashes concatenando en el orden correcto ('L' o 'R')
    for hash_hermano, posicion in prueba:
        if posicion == 'L':
            combinado = hash_hermano + hash_actual
        else:
            combinado = hash_actual + hash_hermano
        
        # Recalcular el hash del nivel inmediatamente superior
        hash_actual = get_hash(combinado)
        
    # 3. Es válido sólo si el resultado final generado coincide con la Merkle Root original
    return hash_actual == merkle_root

def imprimir_diagrama_arbol_5tx(niveles: list):
    """
    Imprime en consola una representación visual tipo diagrama ASCII
    del árbol construido específicamente para 5 transacciones.
    """
    if not niveles or len(niveles) < 4:
        return

    # Extracción de fragmentos de 8 caracteres de los hashes para ajustarse al diagrama visual
    root = niveles[3][0][:8]
    n2_0 = niveles[2][0][:8]
    n2_1 = niveles[2][1][:8]
    n1_0 = niveles[1][0][:8]
    n1_1 = niveles[1][1][:8]
    n1_2 = niveles[1][2][:8]
    
    h0 = niveles[0][0][:8]
    h1 = niveles[0][1][:8]
    h2 = niveles[0][2][:8]
    h3 = niveles[0][3][:8]
    h4 = niveles[0][4][:8]

    diagrama = f"""
================================================================================
                     DIAGRAMA VISUAL DEL ÁRBOL CONSTRUIDO (5 TXs)
================================================================================

                               [{root}] (Merkle Root)
                               /               \\
                  [{n2_0}]                 [{n2_1}] (Duplicado)
                  /          \\              /          \\
          [{n1_0}]          [{n1_1}]    [{n1_2}]          [{n1_2}]
          /     \\          /     \\     /     \\          /     \\
      [{h0}]   [{h1}]    [{h2}]   [{h3}] [{h4}]  [{h4}]    [{h4}]  [{h4}]
        |       |        |       |      |       | (Duplicado)
       T1      T2       T3      T4     T5      T5
================================================================================
"""
    print(diagrama)

def ejecutar_experimento_laboratorio():
    """
    Ejecuta automáticamente la secuencia del experimento del Laboratorio 2.
    """
    print("\n" + "=" * 65)
    print("      EJECUTANDO EXPERIMENTO DEL LABORATORIO (5 TXs)")
    print("=" * 65)

    # Paso 1: Seleccionar las primeras 5 transacciones
    txs = generar_transacciones_base()[:5]
    print("\n[1] Transacciones base creadas:")
    for i, tx in enumerate(txs):
        print(f"  Índice {i} (Transacción {i+1}): {tx}")

    # Paso 2: Construir estructura y obtener la raíz
    niveles = obtener_niveles_arbol(txs)
    root_original = niveles[-1][0]
    print(f"\n[2] Merkle Root calculada:\n    {root_original}")

    # Despliegue del diagrama visual en pantalla
    imprimir_diagrama_arbol_5tx(niveles)

    # Paso 3: Alteración de un dato para probar inmutabilidad
    txs_mod = txs.copy()
    txs_mod[2] = "T3: Carlos paga 999"  # Cambio de monto
    niveles_mod = obtener_niveles_arbol(txs_mod)
    root_mod = niveles_mod[-1][0]
    
    print(f"\n[3] Demostración de inmutabilidad (Modificación de Tx3):")
    print(f"    Transacción alterada : '{txs_mod[2]}'")
    print(f"    Nueva Merkle Root    : {root_mod}")
    print(f"    ¿La raíz se mantuvo idéntica?: {root_original == root_mod}")

    # Paso 4: Generar ruta de inclusión para la Transacción 3 legítima (índice 2)
    tx3_original = txs[2]
    prueba_tx3 = generar_prueba_inclusion(2, niveles)
    print(f"\n[4] Prueba de Inclusión generada para '{tx3_original}':")
    for paso, (hash_h, pos) in enumerate(prueba_tx3, 1):
        print(f"    Paso {paso}: Hermano [{pos}] -> {hash_h[:16]}...")

    # Paso 5: Evaluaciones de prueba de inclusión (Válida e Inválida)
    print("\n[5] Verificación de la prueba de inclusión:")
    
    # Caso 1: Transacción original -> Debe retornar True
    es_valida = verificar_prueba_inclusion(tx3_original, prueba_tx3, root_original)
    print(f"    - Verificación con dato CORRECTO   : {es_valida} (Esperado: True)")

    # Caso 2: Transacción modificada -> Debe retornar False
    dato_falso = "T3: Carlos paga 500"
    es_invalida = verificar_prueba_inclusion(dato_falso, prueba_tx3, root_original)
    print(f"    - Verificación con dato INCORRECTO : {es_invalida} (Esperado: False)")
    print("=" * 65 + "\n")

def mostrar_menu():
    """
    Controlador principal de la interfaz por consola mediante menú iterativo.
    """
    banco_tx = generar_transacciones_base()
    
    while True:
        print("\n" + "*" * 50)
        print("    CONSTRUCTOR DE ÁRBOL DE MERKLE - MENÚ")
        print("*" * 50)
        print("1. Ejecutar Experimento Oficial del Lab (5 Tx + Pruebas)")
        print("2. Seleccionar las primeras N transacciones (1-20)")
        print("3. Seleccionar transacciones específicas por ID (ej: 1, 4, 7)")
        print("4. Ver banco de 20 transacciones")
        print("0. Salir")
        
        opcion = input("\nIngrese una opción: ").strip()

        if opcion == "1":
            ejecutar_experimento_laboratorio()
            input("Presione ENTER para volver al menú...")

        elif opcion == "2":
            try:
                n = int(input("Ingrese la cantidad N (1-20): "))
                if 1 <= n <= 20:
                    sub = banco_tx[:n]
                    niveles = obtener_niveles_arbol(sub)
                    print(f"\nMerkle Root ({n} Tx): {niveles[-1][0]}")
            except ValueError:
                print("Entrada no válida.")

        elif opcion == "3" or "," in opcion:
            # Captura directa de comas o selección por menú secundario
            if opcion == "3":
                indices_str = input("Ingrese IDs separados por coma (ej: 1, 4, 7): ")
            else:
                indices_str = opcion

            try:
                indices = [int(i.strip()) for i in indices_str.split(",") if i.strip()]
                sub = [banco_tx[i - 1] for i in indices if 1 <= i <= 20]
                if sub:
                    niveles = obtener_niveles_arbol(sub)
                    print(f"\nTransacciones seleccionadas ({len(sub)}):")
                    for tx in sub:
                        print(f"  • {tx}")
                    print(f"\nMerkle Root: {niveles[-1][0]}")
                    input("\nPresione ENTER para continuar...")
                else:
                    print("No se seleccionaron IDs válidos entre 1 y 20.")
            except ValueError:
                print("Formato incorrecto. Debe ingresar números separados por comas.")

        elif opcion == "4":
            print("\n--- BANCO DE TRANSACCIONES DISPONIBLES ---")
            for i, tx in enumerate(banco_tx, 1):
                print(f"  [{i:2d}] {tx} -> Hash: {get_hash(tx)}")

        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    mostrar_menu()
