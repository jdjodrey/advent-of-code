import re


def expand_universe(universe):
    new_universe = []
    for line in universe:
        new_universe.append(line)
        if line.count(".") == len(line):
            new_universe.append(line)

    cols_to_expand = []
    for col in range(len(new_universe[0])):
        col_chars = [new_universe[row][col] for row in range(len(new_universe))]
        if col_chars.count(".") == len(col_chars):
            cols_to_expand.append(col)

    for col in cols_to_expand:
        idx = col + cols_to_expand.index(col)
        for row in range(len(new_universe)):
            new_universe[row] = new_universe[row][:idx] + "." + new_universe[row][idx:]

    return new_universe


def main():
    universe = []
    galaxy_pos = []
    with open("../inputs/day11_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            universe.append(line)

    universe = expand_universe(universe)

    for idx, line in enumerate(universe):
        galaxy_x_pos = [m.start() for m in re.finditer("#", line)]
        galaxy_pos += [(idx, x) for x in galaxy_x_pos]

    galaxy_pairs = []
    for idx, galaxy in enumerate(galaxy_pos):
        for galaxy2 in galaxy_pos[idx + 1 :]:
            galaxy_pairs.append((galaxy, galaxy2))

    distances = []
    for pair in galaxy_pairs:
        distance = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        distances.append(distance)

    print(sum(distances))


if __name__ == "__main__":
    main()
