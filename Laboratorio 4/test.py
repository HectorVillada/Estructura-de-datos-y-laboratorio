import matplotlib.pyplot as plt
import random
from Quadtreetree import Point, BoundingBox, QuadTree, brute_force_range_search, brute_force_nearest_neighbor

def plot_quadtree(node, ax):
    """Dibuja recursivamente las divisiones del QuadTree en 2D."""
    mins, maxs = node.boundary.mins, node.boundary.maxs
    width = maxs[0] - mins[0]
    height = maxs[1] - mins[1]
    
    rect = plt.Rectangle((mins[0], mins[1]), width, height, fill=False, edgecolor='gray', linestyle='--', linewidth=0.5)
    ax.add_patch(rect)
    
    if node.divided:
        for child in node.children:
            plot_quadtree(child, ax)

def run_tests_and_visualizations():
    # Semilla para reproducibilidad
    random.seed(42)
    
    # Simular una ciudad de 10,000 m x 10,000 m
    city_size = 10000
    num_points = 10000
    
    points = [Point([random.uniform(0, city_size), random.uniform(0, city_size)], data=i) for i in range(num_points)]
    boundary = BoundingBox([0, 0], [city_size, city_size])
    qt = QuadTree(boundary, capacity=16)
    
    for p in points:
        qt.insert(p)
        
    query_p = Point([5000, 5000])
    radius = 500.0  # 500 metros

    # Búsqueda por Radio
    neighbors_qt = qt.query_range(query_p, radius)
    neighbors_bf = brute_force_range_search(points, query_p, radius)
    
    assert len(neighbors_qt) == len(neighbors_bf), "¡Inconsistencia en la Búsqueda por Radio!"

    # Vecino más Cercano
    nearest_qt, dist_qt = qt.nearest_neighbor(query_p)
    nearest_bf, dist_bf = brute_force_nearest_neighbor(points, query_p)
    
    assert nearest_qt == nearest_bf, "¡Inconsistencia en el Vecino más Cercano!"
    print("✓ Pruebas de consistencia superadas exitosamente.")

    # Generación de gráfica para guardar en el repo
    fig, ax = plt.subplots(figsize=(10, 10))
    plot_quadtree(qt, ax)
    
    # Puntos de la ciudad
    px = [p.coords[0] for p in points]
    py = [p.coords[1] for p in points]
    ax.scatter(px, py, s=3, c='blue', alpha=0.3, label='Puntos de Entrega')
    
    # Puntos dentro del radio
    nx = [p.coords[0] for p in neighbors_qt]
    ny = [p.coords[1] for p in neighbors_qt]
    ax.scatter(nx, ny, s=15, c='green', label=f'Puntos a < {radius}m ({len(neighbors_qt)})')
    
    # Punto de consulta y vecino más cercano
    ax.scatter([query_p.coords[0]], [query_p.coords[1]], c='red', marker='X', s=100, label='Ubicación Consulta')
    ax.scatter([nearest_qt.coords[0]], [nearest_qt.coords[1]], c='orange', marker='o', s=80, label='Más Cercano')
    
    # Dibujar círculo del radio
    circle = plt.Circle((query_p.coords[0], query_p.coords[1]), radius, color='red', fill=False, linewidth=1.5, linestyle='-')
    ax.add_patch(circle)
    
    ax.set_xlim(0, city_size)
    ax.set_ylim(0, city_size)
    ax.set_aspect('equal')
    ax.set_title("Verificación Visual del QuadTree y Búsqueda por Radio (500m)")
    ax.legend(loc='upper right')
    
    plt.savefig("verificacion_quadtree.png", dpi=300)
    print("Imagen 'verificacion_quadtree.png' guardada con éxito.")
    plt.show()

if __name__ == "__main__":
    run_tests_and_visualizations()