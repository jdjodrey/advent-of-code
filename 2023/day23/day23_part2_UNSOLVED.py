import networkx as nx


from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def main():
    trails = []
    with open("../inputs/day23_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        trails = [
            line.replace(">", ".").replace("v", ".") for line in read_data.splitlines()
        ]

    for t in trails:
        print(t)

    def print_hike(path):
        hiked_trail = [[x for x in line] for line in trails]
        for p in path:
            hiked_trail[p[1]][p[0]] = "O"

        hiked_trail[0][1] = "S"
        hiked_trail[p[1]][p[0]] = "E"

        for t in hiked_trail:
            print("".join(t))

        print(f"Path length: {len(path)}")

    graph_id = 0
    G = nx.Graph(id=graph_id)
    graph_id += 1
    graphs = [G]
    debug = False
    visited = set()
    points_to_explore = [(1, 0)]

    def explore(G, points_to_explore, visited, copy_graph=True):
        # print(f"Exploring graph {G.graph['id']} {G}")
        while points_to_explore:
            loc = points_to_explore.pop(0)
            x, y = loc
            visited.add(loc)

            directions_to_check = []
            if y > 0 and trails[y - 1][x] != "#" and (x, y - 1) not in visited:
                directions_to_check.append(Direction.UP)

            if (
                y < len(trails) - 1
                and trails[y + 1][x] != "#"
                and (x, y + 1) not in visited
            ):
                directions_to_check.append(Direction.DOWN)

            if x > 0 and trails[y][x - 1] != "#" and (x - 1, y) not in visited:
                directions_to_check.append(Direction.LEFT)

            if (
                x < len(trails[y]) - 1
                and trails[y][x + 1] != "#"
                and (x + 1, y) not in visited
            ):
                directions_to_check.append(Direction.RIGHT)

            for idx, d in enumerate(directions_to_check):
                dx, dy = d.value
                lx, ly = (x + dx, y + dy)

                next_loc = trails[ly][lx]
                if next_loc == ".":
                    # if loc == (3, 5):
                    #     breakpoint()

                    if idx == 0:
                        if debug:
                            print(f"Adding edge for {loc} -> {(lx, ly)}")
                        G.add_edge(loc, (lx, ly))
                        points_to_explore.append((lx, ly))

                    elif copy_graph:
                        graph_id = int(G.graph["id"]) + 1
                        new_G = nx.Graph(id=graph_id)

                        new_edges = [e for e in G.edges][:-1]
                        new_G.add_edges_from(new_edges)
                        new_visited = visited.copy()
                        new_points = points_to_explore.copy()
                        new_points.pop()
                        new_points.append((lx, ly))

                        # print(f"Graph {new_G.graph['id']}")
                        # print_hike(new_G.nodes)
                        # breakpoint()
                        if debug:
                            print(f"Splitting GRAPH for {loc} -> {(lx, ly)}")
                        new_G.add_edge(loc, (lx, ly))
                        new_G = explore(
                            new_G, new_points, new_visited, copy_graph=False
                        )
                        graphs.append(new_G)

            # print(f"Graph {G.graph['id']}")
            # print_hike(G.nodes)
            # breakpoint()

        if debug:
            print(f"Finished exploring {G}")

        # breakpoint()

        return G

    G = explore(G, points_to_explore, visited)
    graphs.append(G)

    for g in graphs:
        print(25 * "-")
        print_hike(g.nodes)

    # breakpoint()

    # paths = nx.all_simple_paths(G, (1, 0), (139, 140))
    # paths = [p[0] for g in graphs for p in g.edges]
    breakpoint()

    paths = []
    for g in graphs:
        # if (21, 22) in g.nodes:
        if (139, 140) in g.nodes:
            paths.append(len(g.nodes))

    print(f"Longest path is {max(paths) - 1}")

    # breakpoint()
    # longest_path = []
    # for g in graphs:
    #     print(25 * "-")
    #     print_hike(g.nodes)
    # for p in g.nodes:
    #     breakpoint()
    #     p = p[0]
    #     if len(p) > len(longest_path):
    #         longest_path = p
    # breakpoint()
    # print(25 * "-")
    # print_hike(longest_path)
    # print(f"Longest path is {len(longest_path) - 1}")
    # print(25 * "-")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
