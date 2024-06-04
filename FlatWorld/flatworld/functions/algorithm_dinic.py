from math import ceil
import heapq
from .models import Node, Edge, Graf

class PathNotFoundException(Exception):
    pass 

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph.Nodes}
    distances[start] = 0
    queue = [(0, start)]
    visited = set()
    previous_nodes = {}
    previous_edges = {}
    min_flow = float('inf')  # Initialize min_flow to infinity

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        if current_node in visited:
            continue

        visited.add(current_node)

        for edge in graph.Edges:
            if edge.froom == current_node:
                neighbor = edge.to
                distance = current_distance + edge.cost

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    previous_edges[neighbor] = edge
                    heapq.heappush(queue, (distance, neighbor))

    if end not in previous_nodes:
        raise PathNotFoundException("No path found")
    
    path_nodes = []
    path_edges = []
    current = end
    while current is not None:
        path_nodes.append(current)
        if current != start:
            path_edges.append(previous_edges[current])
            # Update min_flow with the minimum flow found so far
            min_flow = min(min_flow, previous_edges[current].flow)
        current = previous_nodes.get(current)
    path_nodes.reverse()
    path_edges.reverse()
    return distances[end], path_nodes, path_edges, min_flow

def dinic(G, start_node, end_node):
    path_available = True
    max_flow = 0
    cost = 0
    while path_available:
        try:
            lowest_cost, path_nodes, path_edges, min_flow = dijkstra(G, start_node, end_node)
            return lowest_cost
            if min_flow == 0:
                raise PathNotFoundException("No path found")
            
            for edge in path_edges:
                cost += edge.cost * min_flow
                edge.flow -= min_flow
                if edge.flow == 0:
                    edge.delete_edge()
            max_flow += min_flow
        except PathNotFoundException:
            path_available = False
            return cost


def calculate_distance(x, y):
    return ((x[0] - y[0])**2 + (x[1] - y[1])**2)**0.5

def calculate_cost(hull_points, world_points, pairs, neighbors):
    distances = []
    hull_points.pop()
    graph = Graf()
    graph.add_node(Node('factory'))
    for i in range(1,len(world_points)+1):
        graph.add_node(Node(str(i)))
    print(neighbors)
    for elem in neighbors:
        graph.add_edge(Edge(graph.Nodes[int(elem[0])], graph.Nodes[int(elem[1])], elem[2], 99999))
    try:
        for i in range(len(hull_points)):
            distances.append(ceil(calculate_distance(hull_points[i], hull_points[i+1])))
    except IndexError:
        distances.append(ceil(calculate_distance(hull_points[i], hull_points[0])))
    cost = 0
    for i in range(len(hull_points)):
        index = world_points.index(hull_points[i])
        index += 1
        distance = dinic(graph, graph.Nodes[0], graph.Nodes[index])
        cost += (distance * distances[i])/pairs
    return cost