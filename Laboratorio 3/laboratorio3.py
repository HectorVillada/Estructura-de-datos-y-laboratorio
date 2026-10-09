import sys
import time
import csv
import random
import statistics
import platform

# ==========================================
# 1. ESTRUCTURAS DE DATOS Y OPERACIONES
# ==========================================

class ListaEstudiantes:
    def __init__(self):
        self.datos = []

    def insertar(self, est):
        self.datos.append(est)

    def buscar(self, id_est):
        for est in self.datos:
            if est["id"] == id_est:
                return est
        return None


class NodoABB:
    def __init__(self, est):
        self.est = est
        self.izq = None
        self.der = None

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, est):
        nuevo_nodo = NodoABB(est)
        if not self.raiz:
            self.raiz = nuevo_nodo
            return
        curr = self.raiz
        clave = est["id"]
        while True:
            if clave < curr.est["id"]:
                if curr.izq is None:
                    curr.izq = nuevo_nodo
                    break
                curr = curr.izq
            else:
                if curr.der is None:
                    curr.der = nuevo_nodo
                    break
                curr = curr.der

    def buscar(self, id_est):
        curr = self.raiz
        while curr:
            if id_est == curr.est["id"]:
                return curr.est
            elif id_est < curr.est["id"]:
                curr = curr.izq
            else:
                curr = curr.der
        return None


class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None

class ArbolBPlus:
    def __init__(self, orden=32):
        self.raiz = NodoBPlus(es_hoja=True)
        self.orden = orden

    def buscar(self, id_est):
        nodo = self.raiz
        while not nodo.es_hoja:
            i = 0
            while i < len(nodo.claves) and id_est >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]
        for idx, k in enumerate(nodo.claves):
            if k == id_est:
                return nodo.hijos[idx]
        return None

    def insertar(self, est):
        clave = est["id"]
        raiz = self.raiz
        if len(raiz.claves) == (self.orden - 1):
            nueva_raiz = NodoBPlus(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self._dividir(nueva_raiz, 0, self.raiz)
            self.raiz = nueva_raiz
            self._insertar_no_lleno(self.raiz, clave, est)
        else:
            self._insertar_no_lleno(raiz, clave, est)

    def _insertar_no_lleno(self, nodo, clave, est):
        i = len(nodo.claves) - 1
        if nodo.es_hoja:
            nodo.claves.append(None)
            nodo.hijos.append(None)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                nodo.hijos[i + 1] = nodo.hijos[i]
                i -= 1
            nodo.claves[i + 1] = clave
            nodo.hijos[i + 1] = est
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == (self.orden - 1):
                self._dividir(nodo, i, nodo.hijos[i])
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave, est)

    def _dividir(self, padre, i, hijo):
        m = self.orden // 2
        nuevo = NodoBPlus(es_hoja=hijo.es_hoja)
        if hijo.es_hoja:
            padre.claves.insert(i, hijo.claves[m])
            padre.hijos.insert(i + 1, nuevo)
            nuevo.claves = hijo.claves[m:]
            nuevo.hijos = hijo.hijos[m:]
            hijo.claves = hijo.claves[:m]
            hijo.hijos = hijo.hijos[:m]
            nuevo.siguiente = hijo.siguiente
            hijo.siguiente = nuevo
        else:
            padre.claves.insert(i, hijo.claves[m - 1])
            padre.hijos.insert(i + 1, nuevo)
            nuevo.claves = hijo.claves[m:]
            nuevo.hijos = hijo.hijos[m:]
            hijo.claves = hijo.claves[:m - 1]
            hijo.hijos = hijo.hijos[:m]

# ==========================================
# 2. METODOLOGÍA ADAPTATIVA
# ==========================================

def generar_datos(n):
    nombres = ["Ana", "Carlos", "Maria", "Juan", "Pedro", "Sofia", "Diego", "Laura"]
    ids = random.sample(range(100000, 9999999), n)
    return [{"id": idx, "nombre": random.choice(nombres)} for idx in ids]

def medir_busquedas(estructura, ids_busqueda):
    t0 = time.perf_counter()
    for id_b in ids_busqueda:
        _ = estructura.buscar(id_b)
    t1 = time.perf_counter()
    return t1 - t0

def ejecutar_experimentos():
    TAMANOS_N = [5000, 10000, 20000, 40000]
    REPETICIONES = 3
    MODOS = ["aleatorios", "ordenados"]

    # Configuración de M calibrada por estructura y modo para lograr tiempos entre 1.0s y 30s
    CONFIG_M = {
        "aleatorios": {
            "Lista": 25000,      # O(N) -> ~1.2s a 15.0s
            "ABB": 4000000,      # O(log N) -> ~1.5s a 2.5s
            "B+": 3000000       # O(log N) -> ~1.2s a 2.0s
        },
        "ordenados": {
            "Lista": 25000,      # O(N) -> ~1.2s a 18.0s
            "ABB": 15000,        # O(N) degenerado -> ~1.1s a 25.0s
            "B+": 3000000       # O(log N) balanceado -> ~1.2s a 2.0s
        }
    }

    resultados_csv = []
    print(f"Iniciando experimentos adaptativos en {platform.system()} ({platform.processor()})...")

    for modo in MODOS:
        for n in TAMANOS_N:
            print(f"\n--- Evaluando N={n} | Datos {modo.upper()} ---")
            
            for estruc_nombre in ["Lista", "ABB", "B+"]:
                m_busquedas = CONFIG_M[modo][estruc_nombre]
                tiempos_corrida = []

                for r in range(REPETICIONES):
                    datos_base = generar_datos(n)
                    if modo == "ordenados":
                        datos_base.sort(key=lambda x: x["id"])

                    if estruc_nombre == "Lista":
                        estruc = ListaEstudiantes()
                    elif estruc_nombre == "ABB":
                        estruc = ABB()
                    else:
                        estruc = ArbolBPlus(orden=32)

                    for est in datos_base:
                        estruc.insertar(est)

                    n_exist = int(m_busquedas * 0.8)
                    n_inexist = m_busquedas - n_exist
                    ids_exist = random.choices([e["id"] for e in datos_base], k=n_exist)
                    ids_inexist = random.choices(range(10000000, 20000000), k=n_inexist)
                    ids_busqueda = ids_exist + ids_inexist
                    random.shuffle(ids_busqueda)

                    t_exp = medir_busquedas(estruc, ids_busqueda)
                    tiempos_corrida.append(t_exp)

                t_prom_total = statistics.mean(tiempos_corrida)
                t_desv_total = statistics.stdev(tiempos_corrida) if REPETICIONES > 1 else 0.0
                
                # Métrica normalizada: Tiempo por búsqueda individual en microsegundos (us)
                us_por_op = (t_prom_total / m_busquedas) * 1e6
                us_desv_op = (t_desv_total / m_busquedas) * 1e6

                resultados_csv.append({
                    "N": n,
                    "M": m_busquedas,
                    "Modo": modo,
                    "Estructura": estruc_nombre,
                    "Tiempo_Total_s": round(t_prom_total, 4),
                    "Promedio_us_op": round(us_por_op, 6),
                    "Desviacion_us_op": round(us_desv_op, 6),
                    "Corridas": REPETICIONES
                })

                print(f"{estruc_nombre:6s} (M={m_busquedas:>8d}) | Tiempo Total: {t_prom_total:6.2f} s | Unidad Ops: {us_por_op:8.4f} µs/op")

    with open("resultados_mediciones.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=resultados_csv[0].keys())
        writer.writeheader()
        writer.writerows(resultados_csv)
    print("\n¡Experimentos adaptativos finalizados exitosamente!")

if __name__ == "__main__":
    ejecutar_experimentos()