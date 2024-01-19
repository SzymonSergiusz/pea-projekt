import pea_utils
import numpy as np

def Pij(alfa, beta, tau, visibility, current_city, S):
    probabilities = []

    # Calculate the numerator for each candidate city j in S
    numerator = [(tau[current_city][j] ** alfa) * (visibility[current_city][j] ** beta) for j in S]

    # Calculate the denominator
    denominator = sum(numerator)

    # Calculate the probabilities for each candidate city
    probabilities = [numerator[i] / denominator for i in range(len(numerator))]

    return probabilities

def ACO(graph, ants, alfa, beta, ro, m, tau0):
    n = len(graph[0])
    visibility = 1 / np.array(graph)  # Calculate visibility as the inverse of distance
    feromony = np.ones((n, n)) * tau0  # Initialize pheromone levels
    best_path = None
    best_cost = float('inf')

    for iteration in range(m):
        ant_paths = []
        ant_distances = []

        for ant in range(ants):
            current_city = np.random.randint(0, n)  # Randomly select the starting city
            S = set(range(n))  # Set of potentially selected cities
            S.remove(current_city)
            path = [current_city]
            distance = 0

            while S:
                probabilities = Pij(alfa, beta, feromony, visibility, current_city, S)
                next_city = np.random.choice(list(S), p=probabilities)
                S.remove(next_city)
                path.append(next_city)
                distance += graph[current_city][next_city]
                current_city = next_city

            distance += graph[path[-1]][path[0]]  # Complete the cycle
            ant_paths.append(path)
            ant_distances.append(distance)

        # Update pheromone levels
        for i in range(n):
            for j in range(n):
                feromony[i][j] *= (1 - ro)  # Evaporation
                for ant in range(ants):
                    if j in ant_paths[ant] and i in ant_paths[ant]:
                        feromony[i][j] += 1 / ant_distances[ant]  # Pheromone deposition

        # Update the best solution if a better one is found
        min_distance = min(ant_distances)
        if min_distance < best_cost:
            best_cost = min_distance
            best_path = ant_paths[ant_distances.index(min_distance)]

    return best_path, best_cost


if __name__ == '__main__':

    graph = pea_utils.file_to_graph('dane/ftv170.txt')

    best_path, best_cost = ACO(graph, ants=10, alfa=1.0, beta=2.0, ro=0.5, m=100, tau0=1.0)
    print("Best Path:", best_path)
    print("Best Cost:", best_cost)
