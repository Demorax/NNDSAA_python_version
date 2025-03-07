import pandas as pd
from typing import Optional
from Coord import Coord
from Dijkstra import Dijkstra
from Graph import Graph
from Road import Road
from City import City
import networkx as nx
import matplotlib.pyplot as plt

import networkx as nx
import matplotlib.pyplot as plt


def visualize_graph(graph):
    G = nx.Graph()

    nodes_data = graph.get_nodes_data()

    for node_id, node_data in nodes_data.items():
        G.add_node(node_id, label=node_data.name)

    edges = graph.get_edges()

    edge_labels = {}
    for (from_id, to_id, edge_data) in edges:
        is_blocked = (from_id, to_id) in graph.get_disabled_edges()
        G.add_edge(from_id, to_id, color="red" if is_blocked else "black")
        edge_labels[(from_id, to_id)] = edge_data.distance

    edge_colors = [G[u][v]["color"] for u, v in G.edges]

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G)
    nx.draw(
        G, pos, with_labels=True,
        labels={n: nodes_data[n].name for n in G.nodes},
        node_color="lightblue", edge_color=edge_colors,
        font_size=14, node_size=2500
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    plt.title("Graph Visualization", fontsize=16)
    plt.show()


def main():
    graph = Graph[str, City, Road]()
    df = pd.read_csv("small.csv")

    for _, row in df.iterrows():
        from_id = row["from"]
        to_id = row["to"]
        weight = row["weight"]
        isBlocked = bool(row["isBlocked"])

        nodes_data = graph.get_nodes_data()

        if from_id not in nodes_data:
            graph.add_node(from_id, City(name=from_id, coordinates=None))
        if to_id not in nodes_data:
            graph.add_node(to_id, City(name=to_id, coordinates=None))

        road = Road(from_id, to_id, weight)
        graph.add_edge(from_id, to_id, road, weight, isBlocked)

    all_keys = set(graph.get_nodes_data().keys())
    adjacencies = {
        key: [(edge[1], edge[2].distance) for edge in graph.get_edges() if edge[0] == key or edge[1] == key]
        for key in all_keys
    }
    disabled_edges = graph.get_disabled_edges()

    dijkstra = Dijkstra(all_keys, adjacencies, disabled_edges)
    result = dijkstra.shortest_path("x")

    print("Distances:", result.distances)
    print("Previous:", result.previous)

    visualize_graph(graph)

if __name__ == "__main__":
    main()