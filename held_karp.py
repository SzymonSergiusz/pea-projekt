from functools import lru_cache
from typing import Tuple, List, Dict


def held_karp(graph) -> Tuple[List, int]:

    S = frozenset(range(1, len(graph)))
    D: Dict[Tuple, int] = {}

    @lru_cache(maxsize=None)
    def distance(d_i: int, S: frozenset) -> int:
        if not S:
            return graph[d_i][0]

        all_costs = [(d_j, graph[d_i][d_j] + distance(d_j, S.difference({d_j}))) for d_j in S]

        n_min, min_cost = min(all_costs, key=lambda x: x[1])

        D[(d_i, S)] = n_min
        return min_cost

    best_dist = distance(0, S)
    d_i = 0
    best_path = [0]

    while S:
        d_i = D[(d_i, S)]
        best_path.append(d_i)
        S = S.difference({d_i})
    return best_path + [0], best_dist


if __name__ == '__main__':
    import pea_utils
    pea_utils.execute_from_ini(held_karp, 'test_atsp.ini')