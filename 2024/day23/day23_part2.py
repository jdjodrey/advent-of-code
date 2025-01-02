import time

import networkx as nx


def main():

    G = nx.Graph()
    with open("../inputs/day23_input.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            label1, label2 = line.split("-")
            G.add_edge(label1, label2)

    cliques = list(nx.find_cliques(G))
    cliques_by_length = {len(c): c for c in cliques}

    biggest_clique_size = max(cliques_by_length.keys())
    biggest_cliques = cliques_by_length[biggest_clique_size]
    print(",".join(sorted(list(set(biggest_cliques)))))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")