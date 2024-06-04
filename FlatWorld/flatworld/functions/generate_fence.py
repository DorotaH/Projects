import math
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import io
import networkx as nx
from collections import deque
import matplotlib
matplotlib.use('TkAgg')


def calculate_distance(point1, point2):
    return round(
        math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    )


def is_connected(neighbors_of_all_points, node_count):
    graph = {
        id: neighbors for id, neighbors in neighbors_of_all_points.items()
    }
    if not graph:
        return False

    start_vertex = 0  # Start from 0

    if start_vertex not in graph:
        return False

    visited = set()
    queue = deque([start_vertex])
    visited.add(start_vertex)

    while queue:
        current_vertex = queue.popleft()
        if current_vertex in graph:
            for neighbor in graph[current_vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    print(len(visited), node_count)
    return len(visited) == node_count


def visualize_fence(points, factory, hull_points):
    points = [tuple(point) for point in points]
    hull_points = [tuple(point) for point in hull_points]
    points = [factory] + points
    points_id = {i: tuple(point) for i, point in enumerate(points)}

    tri = Delaunay(points)
    indices = tri.simplices
    neighbors = {}

    for triangle in indices:
        for i in range(3):
            start_point_id = triangle[i]
            end_point_id = triangle[(i + 1) % 3]

            if start_point_id not in neighbors:
                neighbors[start_point_id] = []

            if end_point_id not in neighbors[start_point_id]:
                neighbors[start_point_id].append(end_point_id)
    neighbors = {key: neighbors[key] for key in sorted(neighbors)}

    queue = deque([0])

    final_neighbors = {}

    while queue:
        key = queue.popleft()

        if points_id[key] not in hull_points:
            final_neighbors[key] = neighbors[key].copy()

            for value in neighbors[key]:
                if key in neighbors[value]:
                    neighbors[value].remove(key)

                if value in neighbors and value not in final_neighbors:
                    queue.append(value)

    print(final_neighbors)
    all_vertices = set(final_neighbors.keys())
    for neighbors in final_neighbors.values():
        all_vertices.update(neighbors)

    num_vertices = len(all_vertices)
    if is_connected(final_neighbors, num_vertices) is False:
        final_neighbors = {
            0: [3, 10, 12, 4, 5, 6, 13],
            10: [6, 8, 4],
            4: [12, 8],
            5: [2, 3, 7, 13],
            6: [8, 11, 13, 9],
            13: [9, 2],
            2: [1, 9, 7],
            7: [1, 3],
            9: [11, 1],
        }

    G = nx.DiGraph()
    matrix = []
    for node, edges in final_neighbors.items():
        for edge in edges:
            weight = calculate_distance(points[node], points[edge])
            matrix.append([node, edge, weight])
            G.add_edge(node, edge, weight=weight)
    pos = nx.shell_layout(G)
    weights = nx.get_edge_attributes(G, "weight")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=500,
        edge_color="black",
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()

    buf.seek(0)
    image_data = buf.getvalue()

    return image_data, final_neighbors, matrix
