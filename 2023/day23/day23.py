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
        trails = [line for line in read_data.splitlines()]

    G = nx.DiGraph()

    def print_hike(path):
        hiked_trail = [[x for x in line] for line in trails]
        for p in path:
            hiked_trail[p[1]][p[0]] = "O"

        for t in hiked_trail:
            print("".join(t))

        print(f"Path length: {len(path)}")

    def get_num_slopes(path):
        num_slopes = 0
        for idx, p in enumerate(path):
            if idx == 0:
                continue

            prev_p = path[idx - 1]
            if abs(p[0] - prev_p[0]) == 2:
                num_slopes += 1
            elif abs(p[1] - prev_p[1]) == 2:
                num_slopes += 1

        return num_slopes

    debug = False
    already_visited = set()
    for y in range(len(trails)):
        for x in range(len(trails[y])):
            if trails[y][x] != ".":
                continue

            loc = (x, y)
            already_visited.add(loc)

            directions_to_check = []
            if y > 0 and trails[y - 1][x] != "#":
                directions_to_check.append(Direction.UP)
            if y < len(trails) - 1 and trails[y + 1][x] != "#":
                directions_to_check.append(Direction.DOWN)
            if x > 0 and trails[y][x - 1] != "#":
                directions_to_check.append(Direction.LEFT)
            if x < len(trails[y]) - 1 and trails[y][x + 1] != "#":
                directions_to_check.append(Direction.RIGHT)

            if debug:
                print(f"{loc} checking {directions_to_check}")
            for d in directions_to_check:
                dx, dy = d.value
                lx, ly = (x + dx, y + dy)

                if (lx, ly) in already_visited:
                    continue

                next_loc = trails[ly][lx]
                if next_loc == ".":
                    if debug:
                        print(f"DOT -> {(lx, ly)} ({trails[ly][lx]})")
                    G.add_edge(loc, (lx, ly))
                    G.add_edge((lx, ly), loc)
                elif next_loc == ">":
                    if d != Direction.LEFT.value:
                        if debug:
                            print(f"> -> {(lx, ly)} ({trails[ly][lx]})")
                        G.add_edge(loc, (lx + 1, ly))
                elif next_loc == "v":
                    if d != Direction.UP.value:
                        if debug:
                            print(f"v -> {(lx, ly)} ({trails[ly][lx]})")
                        G.add_edge(loc, (lx, ly + 1))

    paths = nx.all_simple_paths(G, (1, 0), (139, 140))

    longest_path = []
    for p in paths:
        if len(p) > len(longest_path):
            longest_path = p

    # print_hike(longest_path)
    print(f"Longest path is {len(longest_path) + get_num_slopes(longest_path) - 1}")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
