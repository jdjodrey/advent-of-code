import networkx as nx
from networkx.algorithms.connectivity import is_locally_k_edge_connected


def main():
    G = nx.Graph()

    with open("../inputs/day25_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            n1, nodes = line.split(":")

            for n2 in nodes.split():
                G.add_edge(n1, n2)

    group_a = []
    group_b = []

    node = [n for n in G.nodes][0]
    group_a.append(node)

    for n in G.nodes:
        if node == n:
            continue

        if is_locally_k_edge_connected(G, node, n, 4):
            group_a.append(n)
        else:
            group_b.append(n)

    print(len(group_a) * len(group_b))


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
