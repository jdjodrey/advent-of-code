import time
from enum import Enum

import networkx as nx


class Direction(Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = x, y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Memory:
    def __init__(self, height: int, width: int, corrupted_coords: list[tuple[int, int]]):
        self.height = height
        self.width = width
        self.layout = [["."] * self.width for _ in range(self.height)]

        for x, y in corrupted_coords:
            self.layout[y][x] = "#"

        self.nodes = self._get_nodes()
        self.nodes_by_pos = {n.pos: n for n in self.nodes}

        self.G = nx.Graph()
        self.build_edges()

    def _get_nodes(self) -> list[Node]:
        nodes = []
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                if tile != "#":
                    nodes.append(Node(x, y))

        return nodes

    def build_edges(self):
        for node in self.nodes:
            for adj_node in self._get_adj_nodes(node):
                self.G.add_edge(node, adj_node)

    def _get_adj_nodes(self, node: Node) -> list[Node]:
        adj_nodes: list[Node] = []
        for d in Direction:
            adj_x, adj_y = node.x + d.x, node.y + d.y
            if adj_node := self.nodes_by_pos.get((adj_x, adj_y)):
                adj_nodes.append(adj_node)

        return adj_nodes

    def display(self):
        for row in self.layout:
            print("".join(row))


def main():

    falling_bytes = 2975
    corrupted_coords: list[tuple[int, int]] = []
    with open("../inputs/day18_input.txt", encoding="utf-8") as f:
        for idx, line in enumerate(f.read().splitlines()):
            if idx >= falling_bytes:
                break

            x, y = line.split(",")
            corrupted_coords.append((int(x), int(y)))

    memory = Memory(71, 71, corrupted_coords)
    start = memory.nodes_by_pos[(0, 0)]
    end = memory.nodes_by_pos[(memory.width - 1, memory.height - 1)]
    path = nx.shortest_path(memory.G, start, end)
    print(len(path) - 1)


def print_path(layout, path):
    layout_print: list[list[str]] = []
    for row in layout:
        layout_print.append([x for x in row])

    for node in path:
        layout_print[node.y][node.x] = "O"

    print(15 * "-")
    for row in layout_print:
        print("".join(row))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")