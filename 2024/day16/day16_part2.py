import time
from collections import defaultdict
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
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Maze:
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.start, self.end, self.nodes = self._get_nodes()
        self.nodes_by_pos: dict[tuple[int, int], Node] = {(n.x, n.y): n for n in self.nodes}
        self.visited_nodes: set[tuple[int, int]] = set()

        # Adjacency list with weights, e.g.
        # (1, 1): [(1, 2, 1001), (2, 1, 1)]
        self.adj_nodes: dict[tuple[int, int], list[tuple[Node, int]]] = {}

        self.direction = Direction.E

        self.G = nx.DiGraph()
        self._build_edges()

    def _get_nodes(self) -> tuple[Node, Node, list[Node]]:
        start = None
        end = None
        nodes = []
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                if tile == ".":
                    nodes.append(Node(x, y))
                elif tile == "S":
                    start = Node(x, y)
                    nodes.append(start)
                elif tile == "E":
                    end = Node(x, y)
                    nodes.append(end)

        return start, end, nodes

    def _build_edges(self):

        up_node = self.nodes_by_pos[(self.start.x, self.start.y - 1)]
        self.G.add_edge(self.start, up_node, weight=1001)

        visited_nodes_by_node: dict[Node, set[Node]] = defaultdict(set)
        nodes_to_visit: list[tuple[Node, Direction]] = [(up_node, Direction.N), (self.start, Direction.E)]
        while len(nodes_to_visit):
            node, current_direction = nodes_to_visit.pop(0)
            for adj_node, adj_direction, cost in self._get_adj_nodes(node, current_direction):

                if adj_node not in visited_nodes_by_node[node]:
                    visited_nodes_by_node[node].add(adj_node)

                    self.G.add_edge(node, adj_node, weight=cost)

                    # Don't need to travel further than the end
                    if adj_node != self.end:
                        nodes_to_visit.append((adj_node, adj_direction))

    def _get_adj_nodes(self, node: Node, current_direction: Direction) -> list[tuple[Node, Direction, int]]:
        adj_nodes: list[tuple[Node, Direction, int]] = []

        # The three directions we check are straight, straight-left, and straight-right
        straight_x = node.x + current_direction.x
        straight_y = node.y + current_direction.y

        if current_direction.x == 0:
            # Add East
            east = (node.x + 1, straight_y)
            if adj_node := self.nodes_by_pos.get(east):
                adj_nodes.append((adj_node, Direction.E, 1002))

            # Add West
            west = (node.x - 1, straight_y)
            if adj_node := self.nodes_by_pos.get(west):
                adj_nodes.append((adj_node, Direction.W, 1002))
        elif current_direction.y == 0:
            # Add North
            north = (straight_x, node.y - 1)
            if adj_node := self.nodes_by_pos.get(north):
                adj_nodes.append((adj_node, Direction.N, 1002))

            # Add South
            south = (straight_x, node.y + 1)
            if adj_node := self.nodes_by_pos.get(south):
                adj_nodes.append((adj_node, Direction.S, 1002))

        # If no turns are available, we can go straight one step (or if next step is end)
        if not adj_nodes or self.nodes_by_pos.get((straight_x, straight_y)) == self.end:
            straight_one = (straight_x, straight_y)
            if adj_node := self.nodes_by_pos.get(straight_one):
                adj_nodes.append((adj_node, current_direction, 1))

        # Otherwise, we have to step straight two and skip the intersection node
        else:
            straight_two = node.x + (current_direction.x * 2), node.y + (current_direction.y * 2)
            if adj_node := self.nodes_by_pos.get(straight_two):
                adj_nodes.append((adj_node, current_direction, 2))

        return adj_nodes

    def display(self):
        for row in self.layout:
            print(row)


def main():

    layout: list[str] = []
    with open("../inputs/day16_input.txt", encoding="utf-8") as f:

        for line in f.read().splitlines():
            layout.append(line)

    m = Maze(layout)

    paths = nx.all_shortest_paths(m.G, source=m.start, target=m.end, weight="weight")

    tiles = set()
    for path in paths:

        tiles.update(set(path))
        # Add corners and two-node jumps
        for idx in range(len(path)):
            if idx + 2 == len(path):
                break

            node_v, node_u = path[idx], path[idx + 1]
            # edge contains a turn, so find corner tile
            if node_v.x != node_u.x and node_v.y != node_u.y:
                corner_1 = (node_v.x, node_u.y)
                if corner_1 in m.nodes_by_pos:
                    tiles.add(m.nodes_by_pos[corner_1])
                else:
                    corner_2 = (node_u.x, node_v.y)
                    tiles.add(m.nodes_by_pos[corner_2])

            # edge contains a jump, so find middle tile
            elif abs(node_v.x - node_u.x) == 2 or abs(node_v.y - node_u.y) == 2:
                middle_x = (node_v.x + node_u.x)//2
                middle_y = (node_v.y + node_u.y)//2
                tiles.add(m.nodes_by_pos[(middle_x, middle_y)])

    print(len(tiles))


def print_path(layout, path):
    layout_print: list[list[str]] = []
    for row in layout:
        layout_print.append([x for x in row])

    for node in path:
        layout_print[node.y][node.x] = "X"

    print(15 * "-")
    for row in layout_print:
        print("".join(row))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")