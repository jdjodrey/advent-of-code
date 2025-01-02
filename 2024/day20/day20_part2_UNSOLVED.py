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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))


class Track(Node):
    pass


class Wall(Node):
    def __init__(self, x: int, y: int,):
        self.adj_track_nodes = []
        super().__init__(x, y)

    def set_adj_track_nodes(self, adj_track_nodes: list[Track]):
        self.adj_track_nodes = adj_track_nodes


class Race:
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.start = None
        self.end = None
        self.track_nodes = []
        self.track_nodes_by_pos = {}
        self.track_to_track_dist = {}
        self.wall_nodes = []
        self.wall_nodes_by_pos = {}
        self.wall_to_wall_dist = {}

        self.track_G = nx.Graph()
        self._build_track_nodes()
        self._build_track_edges()
        self._build_track_dist()

        self.wall_G = nx.Graph()
        self._build_wall_nodes()
        self._build_wall_edges()
        self._build_wall_dist()

    def _build_track_nodes(self):
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):

                if tile != "#":
                    track = Track(x, y)
                    self.track_nodes.append(track)
                    self.track_nodes_by_pos[track.pos] = track
                    if tile == "S":
                        self.start = track
                    elif tile == "E":
                        self.end = track

    def _build_track_edges(self):
        for node in self.track_nodes:
            for adj_node in self._get_adj_track_nodes(node):
                self.track_G.add_edge(node, adj_node)

    def _get_adj_track_nodes(self, node: Node) -> list[Track]:
        adj_tracks: list[Track] = []
        for d in Direction:
            adj_x, adj_y = node.x + d.x, node.y + d.y
            if track_node := self.track_nodes_by_pos.get((adj_x, adj_y)):
                adj_tracks.append(track_node)

        return adj_tracks

    def _build_track_dist(self):
        print("Building track distances")

        track_dists: dict[Track, dict[Track, int]] = dict(nx.all_pairs_shortest_path_length(self.track_G))
        print("Track distances built")
        for track_start, track_ends in track_dists.items():

            for track_end, track_dist in track_ends.items():
                if track_start == track_end:
                    continue

                if (track_start.pos, track_end.pos) in self.track_to_track_dist:
                    continue

                self.track_to_track_dist[(track_start.pos, track_end.pos)] = track_dist + 1
                self.track_to_track_dist[(track_end.pos, track_start.pos)] = track_dist + 1

    def _build_wall_nodes(self):
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                wall = Wall(x, y)
                self.wall_nodes.append(wall)
                self.wall_nodes_by_pos[wall.pos] = wall
                wall.set_adj_track_nodes(self._get_adj_track_nodes(wall))

    def _build_wall_edges(self):
        for wall in self.wall_nodes:
            for adj_wall in self._get_adj_wall_nodes(wall):
                self.wall_G.add_edge(wall, adj_wall)

    def _get_adj_wall_nodes(self, wall: Wall) -> list[Wall]:
        adj_walls: list[Wall] = []
        for d in Direction:
            adj_x, adj_y = wall.x + d.x, wall.y + d.y
            if adj_node := self.wall_nodes_by_pos.get((adj_x, adj_y)):
                adj_walls.append(adj_node)

        return adj_walls

    def _build_wall_dist(self):
        print("Building wall-to-wall distances")

        wall_dists: dict[Wall, dict[Wall, int]] = dict(nx.all_pairs_shortest_path_length(self.wall_G, cutoff=19))
        print("Wall distances built")
        for wall_start, wall_ends in wall_dists.items():
            if not wall_start.adj_track_nodes:
                continue

            for wall_end, shortcut_dist in wall_ends.items():
                if not wall_end.adj_track_nodes:
                    continue

                if wall_start == wall_end:
                    continue

                if (wall_start.pos, wall_end.pos) in self.wall_to_wall_dist:
                    continue

                self.wall_to_wall_dist[(wall_start.pos, wall_end.pos)] = shortcut_dist + 1
                self.wall_to_wall_dist[(wall_end.pos, wall_start.pos)] = shortcut_dist + 1

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


def main():

    with open("../inputs/day20_input.txt", encoding="utf-8") as f:
        layout: list[str] = f.read().splitlines()

    r = Race(layout)

    edges_checked = set()
    num_big_short_cuts = 0
    print("Calculating shortcuts")
    for wall_pos, dist in r.wall_to_wall_dist.items():
        wall1, wall2 = r.wall_nodes_by_pos[wall_pos[0]], r.wall_nodes_by_pos[wall_pos[1]]

        for shortcut_start in wall1.adj_track_nodes:
            for shortcut_end in wall2.adj_track_nodes:
                if shortcut_start == shortcut_end:
                    continue

                if (shortcut_start, shortcut_end) in edges_checked:
                    continue

                # the time saved is how far away those points are normally minus the shortcut distance
                time_saved = r.track_to_track_dist[(shortcut_start.pos, shortcut_end.pos)] - dist
                if time_saved >= 100:
                    num_big_short_cuts += 1

                edges_checked.add((shortcut_start, shortcut_end))
                edges_checked.add((shortcut_end, shortcut_start))

    print(num_big_short_cuts)

    # 1141040 is too high
    # 114104 is too low


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")