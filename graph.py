import networkx as nx
import random
import matplotlib.pyplot as plt
from AStar import AStar_pathfinding
from Dijkstra import Dijkstra_pathfinding

def generate_weighted_graph(num_nodes: int, allow_orphans: bool=True, random_weights: bool=False):
    # Create an empty graph
    G = nx.Graph()

    # Add nodes to the graph
    G.add_nodes_from(range(num_nodes))

    # Assign random positions to each node (for heuristic function in A* algorithm)
    pos = {node: (random.uniform(0, 10), random.uniform(0, 10)) for node in G.nodes}
    nx.set_node_attributes(G, pos, 'pos')

    # Generate random edges between nodes with specified weights
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() > 0.5:  # Randomly decide if an edge should exist
                weight = round(random.uniform(0, 1), 2) if random_weights else 1
                G.add_edge(i, j, weight=weight)

    # Ensure no orphan nodes if not allowed
    if not allow_orphans:
        for node in list(G.nodes):
            if G.degree(node) == 0:  # If the node is an orphan
                # Add a random edge to this node to connect it
                potential_nodes = [n for n in G.nodes if n != node]
                target_node = random.choice(potential_nodes)
                weight = round(random.uniform(0, 1), 2) if random_weights else 1
                G.add_edge(node, target_node, weight=weight)

    return G

def get_layout(graph):
    num_nodes = graph.number_of_nodes()
    
    # Adjust layout for graphs with more nodes to spread them out
    if num_nodes >= 10:
        # Increase the 'k' value to space nodes more for larger graphs
        pos = nx.spring_layout(graph, k=15.0/num_nodes, iterations=100)
    else:
        pos = nx.spring_layout(graph)

    return pos

def testDijkstra(num_nodes: int):
    graph = generate_weighted_graph(num_nodes=num_nodes, allow_orphans=True, random_weights=False)
    source = random.randint(0, num_nodes)
    target = random.randint(0, num_nodes)
    
    shortest_distance, path = Dijkstra_pathfinding(graph, source, target)
    
    print("Nodes in the graph:", graph.nodes)
    print(f"Shortest distance from {source} to {target}: {shortest_distance}")
    print("Shortest path:", path)
    
    # Draw the graph with edge labels (weights)
    pos = get_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    nx.draw_networkx_edges(graph, pos, edgelist=list(zip(path, path[1:])), edge_color='r', width=2)

    plt.show()

def testAStar(num_nodes: int):
    graph = generate_weighted_graph(num_nodes=num_nodes, allow_orphans=True, random_weights=False)
    source = random.randint(0, num_nodes)
    target = random.randint(0, num_nodes)

    # Run A* algorithm
    shortest_path = AStar_pathfinding(graph, source, target)
    
    print("Nodes in the graph:", list(graph.nodes))
    print(f"Shortest path from {source} to {target}: {shortest_path}")
    
    if shortest_path is not None:
        pos = get_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='r', width=2)

        plt.show()
    else:
        print("No path found between the source and target.")

def testGraphGen():
    # Parameters
    num_nodes = 12
    allow_orphans = False
    random_weights = False  # Set to False to use equal weights for all edges

    # Generate graph
    graph = generate_weighted_graph(num_nodes, allow_orphans, random_weights)

    # Draw the graph with edge labels (weights)
    pos = get_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.show()
    
if __name__ == "__main__":
    # Run graph generation test
    testGraphGen()

    # Run Dijkstra test
    testDijkstra(15)

    # Run A* test
    testAStar(15)