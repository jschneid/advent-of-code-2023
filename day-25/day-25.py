import networkx as nx
from random import choices

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def build_graph():
    graph = nx.Graph()
    lines = read_input_file_lines()
    for line in lines:
        source, destinations = line.split(': ')
        for destination in destinations.split():
            graph.add_edge(source, destination)
    return graph

def random_node_pair(graph):
    sample = choices(list(graph.nodes), k=2)
    return sample 

def connected_node_count(graph, node_id):
    return len(nx.node_connected_component(graph, node_id))

def three_edges_to_remove(graph):
    average_shortest_path_length_with_edge_removed = {}

    for edge in graph.edges:
        graph.remove_edge(*edge)
        average_shortest_path_length_with_edge_removed[edge] = nx.average_shortest_path_length(graph)
        graph.add_edge(*edge)

    average_shortest_path_length_with_edge_removed = dict(sorted(average_shortest_path_length_with_edge_removed.items(), key=lambda item: item[1] * -1))

    edges_to_remove = {k: average_shortest_path_length_with_edge_removed[k] for k in list(average_shortest_path_length_with_edge_removed)[:3]}

    return edges_to_remove

graph = build_graph()
edges_to_remove = three_edges_to_remove(graph)

for edge in edges_to_remove:
    graph.remove_edge(*edge)

first_key = next(iter(edges_to_remove))
solution = connected_node_count(graph, first_key[0]) * connected_node_count(graph, first_key[1]) 
print(solution)