from typing import List
import networkx as nx
import heapq

def Dijkstra_pathfinding(graph: nx.graph, source: int, target: int):
    unvisited = [(0, source)]
    heapq.heapify(unvisited)
    dist = {node: float('inf') for node in graph.nodes}
    dist[source] = 0.0
    prev = {node: None for node in graph.nodes}

    while unvisited:
        current_distance, current_node = heapq.heappop(unvisited)

        if current_node == target:
            break

        if current_distance > dist[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            temp_distance = dist[current_node] + graph[current_node][neighbor].get('weight', 1)
            if temp_distance < dist[neighbor]:
                dist[neighbor] = temp_distance
                prev[neighbor] = current_node
                heapq.heappush(unvisited, (temp_distance, neighbor))
                
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = prev[current]

    shortest_distance = dist[target]
    return shortest_distance, path    