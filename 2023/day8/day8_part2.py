import re
from math import lcm


def main():
    _map = {}
    current_nodes = []

    with open("../inputs/day8_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            if "=" in line:
                mapping = re.findall(r"(\w\w\w) = \((\w\w\w), (\w\w\w)\)", line)[0]

                start, l, r = mapping[0], mapping[1], mapping[2]
                _map[start] = (l, r)
                if start.endswith("A"):
                    current_nodes.append(start)

            elif len(line) > 1:
                instructions = line.replace("L", "0").replace("R", "1")

    # map out the start -> end nodes
    end_to_end_map = _map.copy()
    for node in end_to_end_map.keys():
        cur = node
        for idx in instructions:
            move = int(idx)
            cur = _map[cur][move]

        end_to_end_map[node] = cur

    # see how many iterations each starting node takes to get to an ending node
    start_to_num_iterations = {}
    times_seen_end = {}
    for j in range(0, len(current_nodes)):
        start = current_nodes[j]
        times_seen_end[start] = 0
        iterations = 0
        while not current_nodes[j].endswith("Z"):
            current_nodes[j] = end_to_end_map[current_nodes[j]]
            iterations += 1
            if current_nodes[j].endswith("Z"):
                times_seen_end[start] += 1

        start_to_num_iterations[start] = iterations

    print(lcm(*start_to_num_iterations.values()) * len(instructions))


if __name__ == "__main__":
    main()
