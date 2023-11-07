import networkx as nx
import random

def generate_atsp_graph(n):
    G = nx.DiGraph()
    graph_array = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                weight = random.randint(1, 100)  # change the range according to your requirements
                G.add_edge(i, j, weight=weight)
                graph_array[i][j] = weight

    return graph_array

def print_graph_as_array(graph_array):
    for row in graph_array:
        print(" ".join(map(str, row)))

if __name__ == '__main__':
    n = 25  # You can change the value of n to the desired dimension
    graph_array = generate_atsp_graph(n)
    print(len(graph_array))
    print_graph_as_array(graph_array)
