import random
import time

# ==========================================
# 0. GENERACIÓN DE DATOS DE ESTUDIANTES
# ==========================================

N_ESTUDIANTES = 10000
N_BUSQUEDAS = 100

def generar_estudiantes(n):
    nombres = ["Ana", "Carlos", "María", "Juan", "Laura", "Pedro", "Sofía", "Diego"]
    # Generamos IDs únicos
    ids = random.sample(range(1000, 1000 + n * 2), n)
    estudiantes = [
        {
            "id": idx,
            "nombre": random.choice(nombres),
            "promedio": round(random.uniform(5.0, 10.0), 1)
        }
        for idx in ids
    ]
    return estudiantes

# ==========================================
# 1. ESTRUCTURA: LISTA SECUENCIAL
# ==========================================

class ListaEstudiantes:
    def __init__(self):
        self.datos = []

    def insertar(self, estudiante):
        self.datos.append(estudiante)

    def buscar(self, id_estudiante):
        for est in self.datos:
            if est["id"] == id_estudiante:
                return est
        return None

# ==========================================
# 2. ESTRUCTURA: ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# ==========================================

class NodoABB:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izq = None
        self.der = None

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):
        if not self.raiz:
            self.raiz = NodoABB(estudiante)
        else:
            self._insertar_recursivo(self.raiz, estudiante)

    def _insertar_recursivo(self, actual, estudiante):
        if estudiante["id"] < actual.estudiante["id"]:
            if actual.izq is None:
                actual.izq = NodoABB(estudiante)
            else:
                self._insertar_recursivo(actual.izq, estudiante)
        else:
            if actual.der is None:
                actual.der = NodoABB(estudiante)
            else:
                self._insertar_recursivo(actual.der, estudiante)

    def buscar(self, id_estudiante):
        return self._buscar_recursivo(self.raiz, id_estudiante)

    def _buscar_recursivo(self, actual, id_estudiante):
        if actual is None or actual.estudiante["id"] == id_estudiante:
            return actual.estudiante if actual else None
        if id_estudiante < actual.estudiante["id"]:
            return self._buscar_recursivo(actual.izq, id_estudiante)
        return self._buscar_recursivo(actual.der, id_estudiante)

# ==========================================
# 3. ESTRUCTURA: ÁRBOL B+ (Simplificado para RAM)
# ==========================================

class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []  # Punteros a nodos hijos (si no es hoja) o datos (si es hoja)
        self.siguiente = None  # Puntero a la siguiente hoja (lista enlazada)

class ArbolBPlus:
    def __init__(self, orden=32):
        self.raiz = NodoBPlus(es_hoja=True)
        self.orden = orden

    def buscar(self, id_estudiante):
        nodo = self.raiz
        while not nodo.es_hoja:
            i = 0
            while i < len(nodo.claves) and id_estudiante >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]
        
        for idx, clave in enumerate(nodo.claves):
            if clave == id_estudiante:
                return nodo.hijos[idx]
        return None

    def insertar(self, estudiante):
        clave = estudiante["id"]
        raiz = self.raiz
        if len(raiz.claves) == (self.orden - 1):
            nueva_raiz = NodoBPlus(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self._dividir_hijo(nueva_raiz, 0, self.raiz)
            self.raiz = nueva_raiz
            self._insertar_no_lleno(self.raiz, clave, estudiante)
        else:
            self._insertar_no_lleno(raiz, clave, estudiante)

    def _insertar_no_lleno(self, nodo, clave, estudiante):
        i = len(nodo.claves) - 1
        if nodo.es_hoja:
            nodo.claves.append(None)
            nodo.hijos.append(None)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                nodo.hijos[i + 1] = nodo.hijos[i]
                i -= 1
            nodo.claves[i + 1] = clave
            nodo.hijos[i + 1] = estudiante
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == (self.orden - 1):
                self._dividir_hijo(nodo, i, nodo.hijos[i])
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave, estudiante)

    def _dividir_hijo(self, padre, i, hijo):
        orden = self.orden
        nuevo_nodo = NodoBPlus(es_hoja=hijo.es_hoja)
        mitad = orden // 2

        if hijo.es_hoja:
            padre.claves.insert(i, hijo.claves[mitad])
            padre.hijos.insert(i + 1, nuevo_nodo)
            
            nuevo_nodo.claves = hijo.claves[mitad:]
            nuevo_nodo.hijos = hijo.hijos[mitad:]
            hijo.claves = hijo.claves[:mitad]
            hijo.hijos = hijo.hijos[:mitad]

            nuevo_nodo.siguiente = hijo.siguiente
            hijo.siguiente = nuevo_nodo
        else:
            padre.claves.insert(i, hijo.claves[mitad - 1])
            padre.hijos.insert(i + 1, nuevo_nodo)

            nuevo_nodo.claves = hijo.claves[mitad:]
            nuevo_nodo.hijos = hijo.hijos[mitad:]
            hijo.claves = hijo.claves[: mitad - 1]
            hijo.hijos = hijo.hijos[:mitad]

# ==========================================
# 4. BENCHMARK / EXPERIMENTO
# ==========================================

def ejecutar_benchmark(datos, titulo):
    print(f"\n==========================================")
    print(f" EXPERIMENTO: {titulo}")
    print(f"==========================================")

    # Instanciar
    lista = ListaEstudiantes()
    abb = ABB()
    bplus = ArbolBPlus(orden=32)

    # Insertar datos
    for est in datos:
        lista.insertar(est)
        abb.insertar(est)
        bplus.insertar(est)

    # Seleccionar 100 IDs aleatorios para buscar
    ids_a_buscar = [random.choice(datos)["id"] for _ in range(N_BUSQUEDAS)]

    # 1. Medir Lista
    inicio = time.time()
    for id_b in ids_a_buscar:
        lista.buscar(id_b)
    tiempo_lista = time.time() - inicio

    # 2. Medir ABB
    inicio = time.time()
    for id_b in ids_a_buscar:
        abb.buscar(id_b)
    tiempo_abb = time.time() - inicio

    # 3. Medir B+
    inicio = time.time()
    for id_b in ids_a_buscar:
        bplus.buscar(id_b)
    tiempo_bplus = time.time() - inicio

    # Imprimir resultados
    print(f"Resultados para {N_BUSQUEDAS} búsquedas en {len(datos)} estudiantes:")
    print(f" - Lista:   {tiempo_lista:.6f} segundos")
    print(f" - ABB:     {tiempo_abb:.6f} segundos")
    print(f" - B+:      {tiempo_bplus:.6f} segundos")

# ==========================================
# EJECUCIÓN DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    # Generar estudiantes
    estudiantes_base = generar_estudiantes(N_ESTUDIANTES)

    # Caso 1: IDs en orden aleatorio (desordenados)
    ejecutar_benchmark(estudiantes_base, "IDs Aleatorios (Árboles Balanceados/Básicos)")

    # Caso 2: IDs en orden secuencial (ordenados)
    estudiantes_ordenados = sorted(estudiantes_base, key=lambda x: x["id"])
    
    # NOTA: Al insertar datos ordenados en un ABB sin balanceo automático (como AVL/Rojo-Negro),
    # el ABB se degrada a O(n), lo que aumentará su tiempo drásticamente o causará un RecursionError.
    import sys
    sys.setrecursionlimit(20000) # Prevenir límite de recursión en ABB desbalanceado
    
    ejecutar_benchmark(estudiantes_ordenados, "IDs Ordenados (Demuestra la degradación del ABB a O(n))")
