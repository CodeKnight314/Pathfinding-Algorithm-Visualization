import networkx as nx

def h(graph, node, goal):
    (x1, y1) = graph.nodes[node]
    (x2, y2) = graph.nodes[goal]
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def AStar_pathfinding(graph: nx.Graph, source: int, target: int):
    open_list = set([source])  # Use a set for efficient membership checks
    closed_list = set()
    g_scores = {node: float('inf') for node in graph.nodes}  # Initialize g scores
    g_scores[source] = 0
    f_scores = {node: float('inf') for node in graph.nodes}  # Initialize f scores
    f_scores[source] = h(graph, source, target)
    came_from = {}  # To store the parent of each node for path reconstruction

    while open_list:
        current = min(open_list, key=lambda node: f_scores[node])  # Get node with lowest f_score
        if current == target:
            # Path found! Reconstruct it
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]  # Reverse the path to get the correct order

        open_list.remove(current)
        closed_list.add(current)

        for neighbor in graph.neighbors(current):
            if neighbor in closed_list:
                continue

            tentative_g_score = g_scores[current] + graph[current][neighbor].get('weight', 1)

            if neighbor not in open_list:
                open_list.add(neighbor)
            elif tentative_g_score >= g_scores[neighbor]:
                continue  # Not a better path

            # This path is the best until now. Record it!
            came_from[neighbor] = current
            g_scores[neighbor] = tentative_g_score
            f_scores[neighbor] = tentative_g_score + h(graph, neighbor, target)

    return None  # No path found