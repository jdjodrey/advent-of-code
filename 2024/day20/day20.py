import time
from collections import defaultdict
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


class Track:
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.start = None
        self.end = None
        self.nodes = []
        self.nodes_by_pos = {}
        self.wall_shortcuts = {}

        self.G = nx.Graph()
        self._build_nodes()
        self._build_edges()

        self.track_length = len(nx.shortest_path(self.G, self.start, self.end))

    def _build_nodes(self):
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):

                if tile != "#":
                    node = Node(x, y)
                    self.nodes.append(node)
                    self.nodes_by_pos[node.pos] = node
                    if tile == "S":
                        self.start = node
                    elif tile == "E":
                        self.end = node

                # If we're not on the edge, check to see if this wall offers a shortcut possibility
                elif 0 < y < len(self.layout) - 1 and 0 < x < len(self.layout[0]) - 1:
                    left_x, left_y, right_x, right_y = x - 1, y, x + 1, y
                    up_x, up_y, down_x, down_y = x, y - 1, x, y + 1
                    left, right = self.layout[left_y][left_x], self.layout[right_y][right_x]
                    up, down = self.layout[up_y][up_x], self.layout[down_y][down_x]

                    # If there's track on either side and walls the other directions, it's a possible shortcut
                    if left != "#" and right != "#" and up == "#" and down == "#":
                        self.wall_shortcuts[(x, y)] = ((left_x, left_y), (right_x, right_y))
                    elif up != "#" and down != "#" and left == "#" and right == "#":
                        self.wall_shortcuts[(x, y)] = ((up_x, up_y), (down_x, down_y))

                    if (4, 1) in self.wall_shortcuts:
                        pass

    def _build_edges(self):
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

    def print_path(self, path: list[Node]):
        layout_print: list[list[str]] = []
        for row in self.layout:
            layout_print.append([x for x in row])

        for node in path:
            if node == self.start:
                layout_print[node.y][node.x] = "S"
            elif node == self.end:
                layout_print[node.y][node.x] = "E"
            else:
                layout_print[node.y][node.x] = "O"

        print(15 * "-")
        for row in layout_print:
            print("".join(row))

    def get_time_saved(self, wall: tuple[int, int]) -> int:
        adj_node1 = self.nodes_by_pos[self.wall_shortcuts[wall][0]]
        adj_node2 = self.nodes_by_pos[self.wall_shortcuts[wall][1]]

        base_length = len(nx.shortest_path(self.G, adj_node1, adj_node2)) - 1

        # the time saved is how far away those points are normally minus the two picoseconds to take the shortcut
        return base_length - 2


def main():

    with open("../inputs/day20_input.txt", encoding="utf-8") as f:
        layout: list[str] = f.read().splitlines()

    t = Track(layout)

    num_big_shortcuts = 0
    for wall_pos in t.wall_shortcuts:
        time_saved = t.get_time_saved(wall_pos)
        if time_saved >= 100:
            num_big_shortcuts += 1

    print(num_big_shortcuts)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")