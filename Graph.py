from typing import MutableMapping, TypeVar, Generic, Tuple, MutableSet, Set, Mapping, List

K = TypeVar('K')
NData = TypeVar('NData')
EData = TypeVar('EData')


class Graph(Generic[K, NData, EData]):
    class Node(Generic[K, NData]):
        def __init__(self, id: K, data: NData):
            self.id: K = id
            self.data: NData = data
            self.edges: MutableMapping[K, "Graph.Edge[K, EData]"] = {}

        def __eq__(self, other) -> bool:
            return self.id == other.id

        def __hash__(self) -> int:
            return hash(self.id)

        def __str__(self) -> str:
            return str(self.id)

    class Edge(Generic[K, EData]):
        def __init__(self, from_node: "Graph.Node[K, NData]", to_node: "Graph.Node[K, NData]", data: EData, isBlocked: bool = False):
            self.from_node: "Graph.Node[K, NData]" = from_node
            self.to_node: "Graph.Node[K, NData]" = to_node
            self.data: EData = data
            self.isBlocked: bool = isBlocked

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Graph.Edge):
                return False
            return (
                self.from_node.id == other.from_node.id and
                self.to_node.id == other.to_node.id and
                self.data == other.data and
                self.isBlocked == other.isBlocked
            )

        def __hash__(self) -> int:
            return hash((self.from_node.id, self.to_node.id, self.data, self.isBlocked))

    __nodes: MutableMapping[K, "Graph.Node[K, NData]"]
    __edges: MutableMapping[Tuple[K, K], float]
    __disabled_edges: Set[Tuple[K, K]]

    def __init__(self):
        self.__nodes: MutableMapping[K, Graph.Node[K, NData]] = {}
        self.__edges: MutableMapping[Tuple[K, K], float] = {}
        self.__disabled_edges: Set[Tuple[K, K]] = set()

    def add_node(self, id: K, data: NData):
        if id not in self.__nodes:
            self.__nodes[id] = Graph.Node(id, data)

    def node_exists(self, id: K) -> bool:
        return id in self.__nodes

    def add_edge(self, from_id: K, to_id: K, data: EData, weight: float, isBlocked: bool):
        from_node = self.__nodes.get(from_id) if from_id in self.__nodes else None
        to_node = self.__nodes.get(to_id) if to_id in self.__nodes else None

        if from_node is None or to_node is None:
            return

        edge = Graph.Edge(from_node, to_node, data, isBlocked)

        from_node.edges[to_id] = edge
        self.__edges[(from_id, to_id)] = weight
        if isBlocked:
            self.__disabled_edges.add((from_id, to_id))

        reversedEdge = Graph.Edge(to_node, from_node, data, isBlocked)
        to_node.edges[from_id] = reversedEdge
        self.__edges[(to_id, from_id)] = weight
        if isBlocked:
            self.__disabled_edges.add((to_id, from_id))

    def disable_edge(self, from_id: K, to_id: K):
        self.__disabled_edges.add((from_id, to_id))
        self.__nodes[from_id].edges[to_id].isBlocked = True

        self.__disabled_edges.add((to_id, from_id))
        self.__nodes[to_id].edges[from_id].isBlocked = True

    def remove_edge(self, from_id: K, to_id: K):
        del self.__edges[(from_id, to_id)]
        del self.__edges[(to_id, from_id)]

        self.__disabled_edges.discard((from_id, to_id))
        self.__disabled_edges.discard((to_id, from_id))

        del self.__nodes[from_id].edges[to_id]
        del self.__nodes[to_id].edges[from_id]

    #Metoda, která vrací veřejnou mapu uzlů: (klíč -> data)
    def get_nodes_data(self) -> Mapping[K, NData]:
        return {key: node.data for key, node in self.__nodes.items()}

    def get_disabled_edges(self) -> Set[Tuple[K, K]]:
        return self.__disabled_edges

    #Metoda, která vrací seznam hran jako trojici: (fromKey, toKey, edgeData)
    def get_edges(self) -> List[Tuple[K, K, EData]]:
        visitedEdges: Set[Tuple[K, K]] = set()
        edges: List[Tuple[K, K, EData]] = []

        for (from_id, node) in self.__nodes.items():
            for (to_id, edge) in node.edges.items():
                pair = (from_id, to_id)
                reverse_pair = (to_id, from_id)

                if pair not in visitedEdges and reverse_pair not in visitedEdges:
                    edges.append((from_id, to_id, edge.data))
                    visitedEdges.add(pair)
                    visitedEdges.add(reverse_pair)

        return edges






