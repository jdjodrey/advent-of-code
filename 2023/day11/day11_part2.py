import re


def expand_universe(universe):
    cols_to_expand = []
    for col in range(len(universe[0])):
        col_chars = [universe[row][col] for row in range(len(universe))]
        if len(set(col_chars)) == 1:
            cols_to_expand.append(col)

    rows_to_expand = []
    for idx, line in enumerate(universe):
        if len(set(line)) == 1:
            rows_to_expand.append(idx)

    return rows_to_expand, cols_to_expand


def main():
    universe = []
    galaxy_pos = []
    with open("../inputs/day11_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            universe.append(line)

    expanded_rows, expanded_cols = expand_universe(universe)

    for idx, line in enumerate(universe):
        galaxy_x_pos = [m.start() for m in re.finditer("#", line)]

        galaxy_pos += [(idx, x) for x in galaxy_x_pos]

    galaxy_pairs = []
    for idx, galaxy in enumerate(galaxy_pos):
        for galaxy2 in galaxy_pos[idx + 1 :]:
            galaxy_pairs.append((galaxy, galaxy2))

    distances = []
    multiple = 1000000
    for pair in galaxy_pairs:
        row_path = (min(pair[0][0], pair[1][0]), max(pair[0][0], pair[1][0]))
        col_path = (min(pair[0][1], pair[1][1]), max(pair[0][1], pair[1][1]))
        distance = abs(row_path[0] - row_path[1]) + abs(col_path[0] - col_path[1])

        crossed_expanded_rows = [
            row for row in expanded_rows if row_path[0] < row < row_path[1]
        ]
        crossed_expanded_cols = [
            col for col in expanded_cols if col_path[0] < col < col_path[1]
        ]

        distance += (len(crossed_expanded_rows) * (multiple - 1)) + (
            len(crossed_expanded_cols) * (multiple - 1)
        )

        distances.append(distance)

    print(sum(distances))


if __name__ == "__main__":
    main()
