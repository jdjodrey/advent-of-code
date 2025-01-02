import time
from enum import Enum

import networkx as nx


class Direction(Enum):
    W = (-1, 0)
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


class Node:
    def __init__(self, x: int, y: int, height: int):
        self.x = x
        self.y = y
        self.height = height

    def __repr__(self):
        return f"({self.x}, {self.y})={self.height}"


class Graph:
    def __init__(self, nodes: list[list[Node]]):
        self.nodes: list[list[Node]] = nodes
        self.trailheads: list[Node] = []
        self.peaks: list[Node] = []

        self.edges: list[tuple[Node, Node]] = []
        self.g = nx.DiGraph()

    def get_trailhead_rating(self) -> int:
        trailhead_rating = 0
        for start in self.trailheads:
            for end in self.peaks:
                try:
                    paths = nx.all_simple_paths(self.g, source=start, target=end)
                except nx.NetworkXNoPath:
                    pass
                else:
                    trailhead_rating += len(list(paths))

        return trailhead_rating

    def build_edges(self):
        for row in self.nodes:
            for node in row:
                if node.height == 0:
                    self.trailheads.append(node)
                elif node.height == 9:
                    self.peaks.append(node)

                for adj_node in self._get_adj_nodes(node):
                    self.edges.append((node, adj_node))

        self.g.add_edges_from(self.edges)

    def _get_adj_nodes(self, node: Node) -> list[Node]:
        adj_nodes: list[Node] = []
        for d in Direction:
            adj_x, adj_y = node.x + d.x, node.y + d.y
            if min(adj_x, adj_y) < 0 or adj_x >= len(self.nodes[0]) or adj_y >= len(self.nodes):
                continue

            adj_node = self.nodes[adj_y][adj_x]
            if adj_node.height == node.height + 1:
                adj_nodes.append(adj_node)

        return adj_nodes


def main():
    nodes: list[list[Node]] = []

    with open("../inputs/day10_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for y, row in enumerate(read_data.splitlines()):
            node_row = []
            for x, height in enumerate([x for x in row]):
                node = Node(x, y, int(height))
                node_row.append(node)

            nodes.append(node_row)

    graph = Graph(nodes)
    graph.build_edges()
    print(graph.get_trailhead_rating())


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
