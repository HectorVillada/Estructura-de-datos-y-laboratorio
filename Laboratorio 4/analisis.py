import time
import random
import matplotlib.pyplot as plt
from Quadtreetree import Point, BoundingBox, QuadTree, brute_force_range_search, brute_force_nearest_neighbor

def measure_performance():
    sizes = [10, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000]
    times_bf_range = []
    times_qt_range = []
    
    num_queries = 50
    radius = 500.0
    city_size = 10000.0

    for N in sizes:
        points = [Point([random.uniform(0, city_size), random.uniform(0, city_size)]) for _ in range(N)]
        queries = [Point([random.uniform(0, city_size), random.uniform(0, city_size)]) for _ in range(num_queries)]
        
        # Construcción QuadTree
        boundary = BoundingBox([0, 0], [city_size, city_size])
        qt = QuadTree(boundary, capacity=16)
        for p in points:
            qt.insert(p)

        # Evaluar Fuerza Bruta
        t0 = time.perf_counter()
        for q in queries:
            brute_force_range_search(points, q, radius)
        t_bf = (time.perf_counter() - t0) / num_queries
        times_bf_range.append(t_bf)

        # Evaluar QuadTree
        t0 = time.perf_counter()
        for q in queries:
            qt.query_range(q, radius)
        t_qt = (time.perf_counter() - t0) / num_queries
        times_qt_range.append(t_qt)

        print(f"N={N:5d} | BF: {t_bf*1000:.4f} ms | QT: {t_qt*1000:.4f} ms")

    # Gráfica de Rendimiento
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, [t * 1000 for t in times_bf_range], label='Fuerza Bruta O(N)', marker='o')
    plt.plot(sizes, [t * 1000 for t in times_qt_range], label='QuadTree O(log N)', marker='s')
    plt.xlabel('Número de Puntos (N)')
    plt.ylabel('Tiempo promedio por consulta (ms)')
    plt.title('Comparativa de Rendimiento: Búsqueda por Radio')
    plt.yscale('log')  # Escala logarítmica para ver claramente el punto de cruce
    plt.xscale('log')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig("rendimiento_comparativo.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    measure_performance()