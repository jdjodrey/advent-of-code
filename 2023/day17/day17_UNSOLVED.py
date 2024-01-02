from collections import defaultdict
import networkx as nx


class Graph:
    def __init__(self, nodes, start):
        self.nodes = nodes
        self.start = start
        self.end = (len(nodes[0]) - 1, len(nodes) - 1)
        self.max_straight_moves = 3
        self.adj_list = self.populate_adj_list(nodes)
        self.unvisited_nodes = self.get_nodes_as_points()
        self.shortest_path = {node: float("inf") for node in self.unvisited_nodes}
        self.prev_nodes = {}

        self.costs = {
            self.start: {
                "cost": 0,
                "prev_node": None,
            }
        }

        self.direction_arrow_map = {
            (1, 0): ">",
            (-1, 0): "<",
            (0, 1): "v",
            (0, -1): "^",
        }

        self.debug_nodes = []

    def get_nodes_as_points(self):
        return [
            (x, y) for y in range(len(self.nodes)) for x in range(len(self.nodes[y]))
        ]

    def set_debug_nodes(self, nodes):
        self.debug_nodes = nodes

    def add_edge(self, from_node, to_node, cost):
        self.adj_list[from_node].append((to_node, cost))

    def get_available_directions(self, cur_node):
        path = self.get_shortest_path(cur_node)
        backwards = (
            (path[-2][0] - path[-1][0], path[-2][1] - path[-1][1])
            if len(path) > 1
            else None
        )

        if len(path) < self.max_straight_moves + 1:
            available_directions = {
                (1, 0): (backwards != (1, 0)),
                (-1, 0): (backwards != (-1, 0)),
                (0, 1): (backwards != (0, 1)),
                (0, -1): (backwards != (0, -1)),
            }
        else:
            back_idx = -(self.max_straight_moves + 1)
            available_directions = {
                (1, 0): path[-1][0] - path[back_idx][0] != self.max_straight_moves,
                (-1, 0): path[back_idx][0] - path[-1][0] != self.max_straight_moves,
                (0, 1): path[-1][1] - path[back_idx][1] != self.max_straight_moves,
                (0, -1): path[back_idx][1] - path[-1][1] != self.max_straight_moves,
            }

            if cur_node in self.debug_nodes:
                print(25 * "-")
                print(
                    f"from {cur_node} can go {[self.direction_arrow_map[x] for x in available_directions if available_directions[x]]} on path {path}"
                )

        return available_directions, backwards

    def get_available_adj_nodes(self, cur_node):
        adj_nodes = self.adj_list[cur_node]
        available_directions, backwards = self.get_available_directions(cur_node)

        available_adj_nodes = []
        unavailable_adj_nodes = []
        for node, cost in adj_nodes:
            increment = (node[0] - cur_node[0], node[1] - cur_node[1])
            if available_directions[increment]:
                available_adj_nodes.append((node, cost))
            else:
                if node != (cur_node[0] + backwards[0], cur_node[1] + backwards[1]):
                    unavailable_adj_nodes.append(node)

        if cur_node in self.debug_nodes:
            print(f"from {cur_node} can go {[x for x in available_adj_nodes]}")

        return available_adj_nodes, unavailable_adj_nodes

    def populate_adj_list(self, nodes):
        adj_list = defaultdict(list)
        for y in range(len(nodes)):
            for x in range(len(nodes[y])):
                adj_nodes = []
                if x > 0:
                    adj_nodes.append((x - 1, y))
                if x < len(nodes[y]) - 1:
                    adj_nodes.append((x + 1, y))
                if y > 0:
                    adj_nodes.append((x, y - 1))
                if y < len(nodes) - 1:
                    adj_nodes.append((x, y + 1))

                cur_node = (x, y)
                for node in adj_nodes:
                    try:
                        nodes[node[1]][node[0]]
                    except IndexError:
                        breakpoint()
                    adj_list[cur_node].append((node, nodes[node[1]][node[0]]))

        return adj_list

    def get_shortest_path(self, end, path=[]):
        if end == self.start:
            return [self.start] + path
        else:
            return self.get_shortest_path(self.prev_nodes[end], path=[end] + path)

    def print_adj_list(self):
        """
        Example:
        (0, 0) --> [((1, 0), 4), ((0, 1), 3)]
        (1, 0) --> [((0, 0), 2), ((2, 0), 1), ((1, 1), 2)]
        (2, 0) --> [((1, 0), 4), ((3, 0), 3), ((2, 1), 1)]
        (3, 0) --> [((2, 0), 1), ((4, 0), 4), ((3, 1), 5)]
        (4, 0) --> [((3, 0), 3), ((5, 0), 3), ((4, 1), 4)]
        (5, 0) --> [((4, 0), 4), ((6, 0), 2), ((5, 1), 5)]
        (6, 0) --> [((5, 0), 3), ((7, 0), 3), ((6, 1), 3)]
        (7, 0) --> [((6, 0), 2), ((8, 0), 1), ((7, 1), 5)]
        """
        for node in self.adj_list:
            print(f"{node} --> {[x for x in self.adj_list[node]]}")

    def print_shortest_path(self, end, path="DONE"):
        if end == self.start:
            print(f"{self.start} --> {path}")
        else:
            self.print_shortest_path(self.prev_nodes[end], path=f"{end} --> {path}")

    def print_shortest_path_v2(self, end=None):
        display_nodes = [[x for x in row] for row in self.nodes]
        path = self.get_shortest_path(end or self.end)
        for idx, step in enumerate(path):
            x, y = step
            if step != self.start:
                prev_step = path[idx - 1]
                increment = (x - prev_step[0], y - prev_step[1])
                display_nodes[y][x] = self.direction_arrow_map[increment]
                # nodes[y][x] = "#"

        for row in display_nodes:
            print("".join([str(x) for x in row]))


def main():
    nodes = []
    with open("../inputs/day17_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            nodes.append([int(x) for x in line])

    start = (0, 0)
    graph = Graph(nodes, start)

    graph.shortest_path[start] = 0

    debug = False

    while graph.unvisited_nodes:
        print(f"Unvisited nodes: {len(graph.unvisited_nodes)}")
        cur_node = None
        for node in graph.unvisited_nodes:
            if (
                cur_node is None
                or graph.shortest_path[node] < graph.shortest_path[cur_node]
            ):
                cur_node = node

        avail_adj_nodes, blocked_adj_nodes = graph.get_available_adj_nodes(cur_node)
        for adj_node, adj_cost in avail_adj_nodes:
            cost = graph.shortest_path[cur_node] + adj_cost
            if cost < graph.shortest_path[adj_node]:
                graph.shortest_path[adj_node] = cost

                graph.prev_nodes[adj_node] = cur_node

        if len(blocked_adj_nodes) == 0:
            graph.unvisited_nodes.remove(cur_node)

    print(f"Minimal path cost: {graph.shortest_path[graph.end]}")
    print(graph.end)
    graph.print_shortest_path_v2(graph.end)


def main_v2():
    nodes = []
    with open("../inputs/day17_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            nodes.append([int(x) for x in line])

    G = nx.DiGraph()

    def get_edge_weight(dest, path, nodes):
        return nodes[dest[1]][dest[0]] + sum([nodes[p[1]][p[0]] for p in path])

    def add_edge_to_graph(G, src, dest, path, nodes):
        try:
            weight = get_edge_weight(dest, path, nodes)
        except IndexError:
            breakpoint()

        if (src, dest) not in G.edges:
            print(f"Adding edge from {src} to {dest} with weight {weight}")
            G.add_edge(src, dest, weight=weight)

        # if we already have an edge to this node, check if the new edge is shorter
        else:
            if weight < G.edges[(src, dest)]["weight"]:
                print(f"Adding shorter edge from {src} to {dest} with weight {weight}")
                G.add_edge(src, dest, weight=weight)

    for y in range(len(nodes)):
        for x in range(len(nodes[y])):
            # can we go up?
            if y > 0:
                right_max = min(len(nodes[y]), x + 4)
                for idx, x2 in enumerate(range(x + 1, right_max)):
                    dest = (x2, y - 1)

                    # add edges with in-between points for >^, >>^, and >>>^
                    path = [(x + n, y) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add edges with in-between points for ^>, ^>> and ^>>>
                    path = [(x + n, y - 1) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                left_max = max(0, x - 4)
                for idx, x2 in enumerate(range(x - 1, left_max, -1)):
                    # add edges with in-between points for <^, <<^, and <<<^
                    dest = (x2, y - 1)
                    path = [(x - n, y) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add edges with in-between points for ^<< and ^<<<
                    dest = (x2, y - 1)
                    path = [(x - n, y - 1) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

            # can we go down?
            if y < len(nodes) - 1:
                right_max = min(len(nodes[y]), x + 4)
                for idx, x2 in enumerate(range(x + 1, right_max)):
                    dest = (x2, y + 1)

                    # add edges with in-between points for >v, >>v, and >>>v
                    path = [(x + n, y) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add edges with in-between points for v>, v>>, and v>>>
                    path = [(x + n, y + 1) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                left_max = max(0, x - 4)
                for idx, x2 in enumerate(range(x - 1, left_max, -1)):
                    dest = (x2, y + 1)

                    # add edges with in-between points for <v, <<v, and <<<v
                    path = [(x - n, y) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add eddges with in-between points for v<, v<<, and v<<<
                    path = [(x - n, y + 1) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

            # can we go left?
            if x > 0:
                down_max = min(len(nodes), y + 4)
                for idx, y2 in enumerate(range(y + 1, down_max)):
                    dest = (x - 1, y2)

                    # add edges with in-between points for v<, vv<, and vvv<
                    path = [(x, y + n) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add edges with in-between points for <v, <vv, and <vvv
                    path = [(x - 1, y + n) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                up_max = min(3, y)
                for idx, y2 in enumerate(range(y - 1, up_max, -1)):
                    dest = (x - 1, y2)

                    # add edges with in-between points for ^<, ^^<, and ^^^<
                    path = [(x, y - n) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add edges with in-between points for <^, <^^, and <^^^
                    path = [(x - 1, y - n) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

            # can we go right?
            if x < len(nodes[y]) - 1:
                down_max = min(len(nodes), y + 4)
                for idx, y2 in enumerate(range(y + 1, down_max)):
                    dest = (x + 1, y2)

                    # add edges with in-between points for v>, vv>, and vvv>
                    path = [(x, y + n) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add edges with in-between points for >v, >vv, and >vvv
                    path = [(x + 1, y + n) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                up_max = min(3, y)
                for idx, y2 in enumerate(range(y - 1, up_max, -1)):
                    dest = (x + 1, y2)

                    # add edges with in-between points for ^>, ^^>, and ^^^>
                    path = [(x, y2 - n) for n in range(1, idx + 2)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

                    # add edges with in-between points for >^, >^^, and >^^^
                    path = [(x + 1, y2 - n) for n in range(0, idx + 1)]
                    add_edge_to_graph(G, (x, y), dest, path, nodes)

    print(nx.shortest_path_length(G, source=(0, 0), target=(x, y), weight="weight"))

    shortest_path = nx.shortest_path(G, source=(0, 0), target=(x, y))
    for idx, src in enumerate(shortest_path):
        if idx == len(shortest_path) - 1:
            break
        dest = shortest_path[idx + 1]
        weight = G.edges[(src, dest)]["weight"]
        print(f"{src} -> {dest} costs {weight}")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
