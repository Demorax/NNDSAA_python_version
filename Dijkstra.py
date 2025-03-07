from typing import TypeVar, Generic, Set, List, Tuple, Mapping, Optional, Dict
import heapq

K = TypeVar('K')

class ShortestPathResult(Generic[K]):
    distances: Dict[K, float]
    previous: Dict[K, Optional[K]]

    def __init__(self, distances: Dict[K, float], previous: Dict[K, Optional[K]]):
        self.distances = distances
        self.previous = previous


class Dijkstra(Generic[K]):

    __all_keys: Set[K]
    __adjacencies: Dict[K, List[Tuple[K, float]]]
    __disabled_edges: Set[Tuple[K, K]]

    def __init__(self, all_keys: Set[K], adjacencies: Dict[K, List[Tuple[K, float]]], disabled_edges: Set[Tuple[K, K]]):
        self.__all_keys = all_keys
        self.__adjacencies = adjacencies
        self.__disabled_edges = disabled_edges

    def shortest_path(self, source: K) -> ShortestPathResult[K]:
        distances: Dict[K, float] = {}
        previous: Dict[K, Optional[K]] = {}

        for key in self.__all_keys:
            distances[key] = float('inf')
            previous[key] = None

        distances[source] = 0.0

        queue: List[Tuple[K, float]] = [(distances[source], source)]
        heapq.heapify(queue)

        while queue:
            current_distance, current = heapq.heappop(queue)

            if current_distance > distances[current]:
                continue

            for neighbor, weight in self.__adjacencies.get(current, []):
                pair = self.__sorted_pair(current, neighbor)
                if pair in self.__disabled_edges:
                    continue

                new_distance = distances[current] + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(queue, (new_distance, neighbor))


        return ShortestPathResult(distances, previous)


    def __sorted_pair(self, a: K, b: K) -> Tuple[K, K]:
        """Returns a sorted tuple of two nodes to maintain consistency."""
        return (a, b) if hash(a) <= hash(b) else (b, a)
