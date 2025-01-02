import time

import networkx as nx


def main():

    G = nx.Graph()
    with open("../inputs/day23_input.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            label1, label2 = line.split("-")
            G.add_edge(label1, label2)

    cycles = list(nx.simple_cycles(G, length_bound=3))
    cycles_with_t_nodes = []
    for c in cycles:
        if any([n.startswith("t") for n in c]):
            cycles_with_t_nodes.append(c)

    print(len(cycles_with_t_nodes))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")