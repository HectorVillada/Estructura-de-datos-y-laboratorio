import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos guardados en el CSV
df = pd.read_csv("resultados_mediciones.csv")

# Estilo de gráfico en matplotlib puro
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({'font.size': 10, 'figure.autolayout': True})

# ---------------------------------------------------------
# GRAFICA 1: Tiempos Totales de Ejecución (Verificación Rule >= 1.0s)
# ---------------------------------------------------------
plt.figure(figsize=(9, 5.5), dpi=300)
for modo, ls in zip(["aleatorios", "ordenados"], ["-", "--"]):
    for estruc, color in zip(["Lista", "ABB", "B+"], ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        sub = df[(df["Modo"] == modo) & (df["Estructura"] == estruc)]
        plt.plot(sub["N"], sub["Tiempo_Total_s"], label=f"{estruc} ({modo.capitalize()})",
                 marker='o', linestyle=ls, color=color, linewidth=2)

plt.axhline(y=1.0, color='r', linestyle=':', label='Umbral Mínimo Requerido (1.0 s)')
plt.title("1. Cumplimiento Metodológico: Tiempo Total de Ejecución (N ∈ [5000, 40000])", fontweight='bold')
plt.xlabel("Tamaño de Entrada N")
plt.ylabel("Tiempo Total de Ejecución (segundos)")
plt.yscale("log")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.savefig("fig1_tiempos_totales_cumplimiento.png")
plt.close()

# ---------------------------------------------------------
# GRAFICA 2: Comparativa de Complejidad Normalizada (µs por Búsqueda)
# ---------------------------------------------------------
plt.figure(figsize=(9, 5.5), dpi=300)
for modo, ls in zip(["aleatorios", "ordenados"], ["-", "--"]):
    for estruc, color in zip(["Lista", "ABB", "B+"], ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        sub = df[(df["Modo"] == modo) & (df["Estructura"] == estruc)]
        plt.errorbar(sub["N"], sub["Promedio_us_op"], yerr=sub["Desviacion_us_op"],
                     label=f"{estruc} ({modo.capitalize()})", marker='s', linestyle=ls, color=color, capsize=3)

plt.title("2. Eficiencia Unitaria Normalizada: Tiempo Promedio por Búsqueda Individual", fontweight='bold')
plt.xlabel("Tamaño de Entrada N")
plt.ylabel("Tiempo por Búsqueda (µs/op - Escala Log)")
plt.yscale("log")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.savefig("fig2_eficiencia_unitaria_normalizada.png")
plt.close()

# ---------------------------------------------------------
# GRAFICA 3: Colapso del ABB frente al Balanceo Continuo del B+
# ---------------------------------------------------------
plt.figure(figsize=(8, 5), dpi=300)
sub_ord = df[df["Modo"] == "ordenados"]
for estruc, color, marker in zip(["ABB", "B+"], ["#d62728", "#2ca02c"], ["x", "o"]):
    sub = sub_ord[sub_ord["Estructura"] == estruc]
    plt.plot(sub["N"], sub["Promedio_us_op"], label=f"{estruc} (Ordenados)", marker=marker, color=color, linewidth=2.5)

plt.title("3. Impacto del Ordenamiento: ABB (Degradación O(N)) vs Árbol B+ (O(log N))", fontweight='bold')
plt.xlabel("Tamaño de Entrada N")
plt.ylabel("Tiempo por Búsqueda (µs/op)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("fig3_abb_vs_bplus_ordenados.png")
plt.close()

# ---------------------------------------------------------
# GRAFICA 4: Sensibilidad de Entrada (Aleatorio vs Ordenado) en N=40000
# ---------------------------------------------------------
plt.figure(figsize=(8, 5), dpi=300)
sub_nmax = df[df["N"] == df["N"].max()]
estructuras = ["Lista", "ABB", "B+"]
x = range(len(estructuras))
width = 0.35

val_aleat = [sub_nmax[(sub_nmax["Estructura"]==e) & (sub_nmax["Modo"]=="aleatorios")]["Promedio_us_op"].values[0] for e in estructuras]
val_ord = [sub_nmax[(sub_nmax["Estructura"]==e) & (sub_nmax["Modo"]=="ordenados")]["Promedio_us_op"].values[0] for e in estructuras]

plt.bar([i - width/2 for i in x], val_aleat, width, label='Aleatorios', color='#66c2a5')
plt.bar([i + width/2 for i in x], val_ord, width, label='Ordenados', color='#fc8d62')

plt.xticks(x, estructuras)
plt.title(f"4. Sensibilidad al Patrón de Entrada en Tamaño Máximo (N={df['N'].max()})", fontweight='bold')
plt.xlabel("Estructura de Datos")
plt.ylabel("Tiempo por Búsqueda (µs/op)")
plt.yscale("log")
plt.legend()
plt.grid(axis='y', linestyle="--", alpha=0.6)
plt.savefig("fig4_sensibilidad_patron_entrada.png")
plt.close()

# ---------------------------------------------------------
# GRAFICA 5: Relación M asignado vs Tiempo Medido Total
# ---------------------------------------------------------
plt.figure(figsize=(8, 5), dpi=300)
for estruc, marker in zip(["Lista", "ABB", "B+"], ["o", "s", "^"]):
    sub = df[df["Estructura"] == estruc]
    plt.scatter(sub["M"], sub["Tiempo_Total_s"], label=f"{estruc}", marker=marker, s=80, alpha=0.8)

plt.title("5. Relación entre Operaciones Solicitadas (M) y Tiempo Medido Total", fontweight='bold')
plt.xlabel("Número de Búsquedas Ejecutadas (M)")
plt.ylabel("Tiempo Total Registrado (segundos)")
plt.xscale("log")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("fig5_relacion_m_vs_tiempo_total.png")
plt.close()

# ---------------------------------------------------------
# GRAFICA 6: Estabilidad Estadística (Coeficiente de Variación CV)
# ---------------------------------------------------------
plt.figure(figsize=(8, 5), dpi=300)
df["CV_%"] = (df["Desviacion_us_op"] / df["Promedio_us_op"]) * 100
for estruc in ["Lista", "ABB", "B+"]:
    sub = df[(df["Estructura"] == estruc) & (df["Modo"] == "aleatorios")]
    plt.plot(sub["N"], sub["CV_%"], label=f"{estruc} (CV %)", marker='d', linewidth=1.8)

plt.title("6. Estabilidad Estadística de Mediciones: Coeficiente de Variación (% CV)", fontweight='bold')
plt.xlabel("Tamaño de Entrada N")
plt.ylabel("Coeficiente de Variación CV = (σ / µ) * 100")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("fig6_coeficiente_variacion.png")
plt.close()

print("¡Las 6 gráficas explicativas se generaron correctamente!")