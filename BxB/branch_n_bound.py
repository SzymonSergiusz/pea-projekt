from __future__ import annotations
# from pea_utils import execute_from_ini
from typing import List
from queue import PriorityQueue

import python_tsp.exact

import pea_utils


class Node:
    parent: 'Node'
    city_index: int
    level: int
    path: list = []
    cost: int

    def __init__(self, parent: 'Node', city_index=0, cost=0):
        # root
        if parent is None:
            self.city_index = 0
            self.level = 0
            self.cost = 0
            self.path = [0]
        else:
            self.parent = parent
            self.city_index = city_index
            self.level = parent.level + 1
            self.cost = parent.cost + cost
            self.path = parent.path + [city_index]

    def __lt__(self, other):
        return self.cost < other.cost


def lower_bound(graph: List[List[int]], path: List[int]) -> int:
    bound = 0
    last_city = path[-1]
    unvisited = [city for city in range(len(graph)) if city not in path]
    for i in range(len(path) - 1):
        bound += graph[path[i]][path[i + 1]]
    if unvisited:
        bound += min([graph[last_city][city] for city in unvisited])
    return bound


def best_first(graph) -> (list, int):
    best_path = []
    best_tour = float('inf')
    pq = PriorityQueue()
    n = len(graph)
    root = Node(parent=None)
    pq.put(root)
    lb = lower_bound(graph, root.path)
    while not pq.empty():

        node: Node = pq.get()
        if lb < best_tour:

            if node.level == n - 1:
                path = node.path + [0]
                cost = node.cost + graph[node.city_index][0]

                if cost < best_tour:
                    best_tour = cost
                    best_path = path

            for city in range(n):

                is_new_node = graph[node.city_index][city] != 0
                if is_new_node and city not in node.path:

                    new_node = Node(parent=node, city_index=city, cost=graph[node.city_index][city])
                    lb = lower_bound(graph, new_node.path)
                    if lb < best_tour:
                        pq.put(new_node)
    return best_path, best_tour


if __name__ == '__main__':
    import pea_utils
    pea_utils.execute_from_ini(best_first, 'test_atsp_bb.ini')