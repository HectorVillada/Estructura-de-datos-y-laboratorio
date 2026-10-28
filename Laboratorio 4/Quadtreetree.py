import math

class Point:
    def __init__(self, coords, data=None):
        self.coords = tuple(coords)  # tuple de K dimensiones (ej. (x, y))
        self.dim = len(coords)
        self.data = data

    def distance_to(self, other_point):
        """Distancia euclidiana en K dimensiones."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.coords, other_point.coords)))


class BoundingBox:
    def __init__(self, mins, maxs):
        self.mins = list(mins)  # Límites inferiores por dimensión
        self.maxs = list(maxs)  # Límites superiores por dimensión
        self.dim = len(mins)

    def contains(self, point):
        """Verifica si un punto está dentro de la región."""
        return all(self.mins[i] <= point.coords[i] <= self.maxs[i] for i in range(self.dim))

    def intersects_sphere(self, center_point, radius):
        """
        Verifica si la región del nodo se traslapa con una hiperesfera (radio r).
        Calcula la distancia mínima desde el centro al hipercubo.
        """
        d_min_sq = 0.0
        for i in range(self.dim):
            c = center_point.coords[i]
            if c < self.mins[i]:
                d_min_sq += (c - self.mins[i]) ** 2
            elif c > self.maxs[i]:
                d_min_sq += (c - self.maxs[i]) ** 2
        return d_min_sq <= (radius ** 2)


class QuadTree:
    def __init__(self, boundary, capacity=4, max_depth=10, depth=0):
        self.boundary = boundary
        self.capacity = capacity
        self.max_depth = max_depth
        self.depth = depth
        self.points = []
        self.children = []  # Tendrá 2^K hijos al subdividir
        self.divided = False

    def subdivide(self):
        """Subdivide el nodo en 2^K hipercuadrantes."""
        k = self.boundary.dim
        num_children = 2 ** k
        midpoints = [(self.boundary.mins[i] + self.boundary.maxs[i]) / 2.0 for i in range(k)]

        for i in range(num_children):
            child_mins = []
            child_maxs = []
            for dim in range(k):
                # El bit 'dim' determina si tomamos la mitad inferior o superior
                if (i >> dim) & 1:
                    child_mins.append(midpoints[dim])
                    child_maxs.append(self.boundary.maxs[dim])
                else:
                    child_mins.append(self.boundary.mins[dim])
                    child_maxs.append(midpoints[dim])
            
            sub_box = BoundingBox(child_mins, child_maxs)
            self.children.append(QuadTree(sub_box, self.capacity, self.max_depth, self.depth + 1))
        
        self.divided = True

    def insert(self, point):
        """Inserta un punto en el árbol."""
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity or self.depth >= self.max_depth:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(point):
                return True

        return False

    def query_range(self, center_point, radius, found_points=None):
        """Búsqueda por rango (Range Search) dentro de un radio r."""
        if found_points is None:
            found_points = []

        # Si el rango no interseca esta región, no hay nada que buscar aquí
        if not self.boundary.intersects_sphere(center_point, radius):
            return found_points

        # Chequear los puntos contenidos en este nodo
        for p in self.points:
            if center_point.distance_to(p) <= radius:
                found_points.append(p)

        # Recorrer los hijos si está subdividido
        if self.divided:
            for child in self.children:
                child.query_range(center_point, radius, found_points)

        return found_points

    def nearest_neighbor(self, target_point):
        """Encuentra el punto más cercano a un punto dado."""
        best = {'point': None, 'dist': float('inf')}

        def _search(node):
            if node is None:
                return

            # Revisar puntos en el nodo actual
            for p in node.points:
                d = target_point.distance_to(p)
                if d < best['dist']:
                    best['dist'] = d
                    best['point'] = p

            if not node.divided:
                return

            # Ordenar hijos por distancia mínima esperada desde target_point para optimizar podas
            def min_dist_to_box(child):
                d_sq = 0.0
                for i in range(child.boundary.dim):
                    c = target_point.coords[i]
                    if c < child.boundary.mins[i]:
                        d_sq += (c - child.boundary.mins[i]) ** 2
                    elif c > child.boundary.maxs[i]:
                        d_sq += (c - child.boundary.maxs[i]) ** 2
                return math.sqrt(d_sq)

            sorted_children = sorted(node.children, key=min_dist_to_box)

            for child in sorted_children:
                if min_dist_to_box(child) < best['dist']:
                    _search(child)

        _search(self)
        return best['point'], best['dist']


# Algoritmo de Fuerza Bruta para Comparación
def brute_force_range_search(points, center_point, radius):
    return [p for p in points if center_point.distance_to(p) <= radius]

def brute_force_nearest_neighbor(points, target_point):
    best_p = None
    best_dist = float('inf')
    for p in points:
        d = target_point.distance_to(p)
        if d < best_dist:
            best_dist = d
            best_p = p
    return best_p, best_dist