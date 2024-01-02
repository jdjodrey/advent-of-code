def print_rocks(rocks):
    for idx, rock in enumerate(rocks):
        print("{0: <3}{1}".format(idx + 1, "".join(rock)))


def get_slide_index(idx, row):
    while idx + 1 < len(row) and row[idx + 1] == ".":
        idx += 1

    return idx


def rotate_90_deg(rocks):
    return [list(x) for x in list(zip(*reversed(rocks)))]


def rotate_to_north(num_rotations, rocks):
    """
    Rotate the rocks so that North (Up) is now East (Right)
    We start facing up, so after 1 rotation we should be facing right
    1 -> 0
    2 -> 3
    3 -> 2
    4 -> 1
    5 -> 0
    6 -> 3
    7 -> 2
    8 -> 1
    9 -> 0
    """
    mod = num_rotations % 4
    rotations_to_north = (4 - mod) if mod != 0 else mod
    for _ in range(rotations_to_north):
        rocks = rotate_90_deg(rocks)

    return rocks


def calculate_load_to_north(rocks):
    load = 0
    max_load = len(rocks)
    for idx, row in enumerate(rocks):
        num_rocks = row.count("O")
        load += (max_load - idx) * num_rocks

    return load


def find_billionth_load(loads):
    pattern_start = None
    pattern_length = None

    # guess that the pattern repetition is between 5 and 20 elements long
    for x in range(5, 20):
        if pattern_start:
            break
        for idx in range(len(loads) - x):
            if loads[idx : idx + x] == loads[idx + x : idx + (2 * x)]:
                print(f"Found Pattern: {loads[idx:idx + x]} at {idx} of length {x}")
                pattern_start = idx
                pattern_length = x
                break

    loads = loads[pattern_start:]
    billionth_index = (1000000000 - 1 - pattern_start) % pattern_length
    print(f"Billionth Index: {billionth_index} of the pattern")

    return loads[billionth_index]


def main():
    rocks = []
    with open("../inputs/day14_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            rocks.append([x for x in line])

    # rotate 90 degrees clockwise, so North (Up) is now East (Right)
    num_cycles = 250
    num_rotations = 4 * num_cycles
    loads = []
    for ridx in range(num_rotations):
        rocks = rotate_90_deg(rocks)

        # iterate from the end of each row to the beginning
        for row in rocks:
            for idx in range(len(row) - 2, -1, -1):
                if row[idx] == "O" and (slide_index := get_slide_index(idx, row)):
                    row[idx] = "."
                    row[slide_index] = "O"

        # every 4 rotations is a cycle
        if (ridx + 1) % 4 == 0:
            load = calculate_load_to_north(rocks)
            loads.append(load)

    print(find_billionth_load(loads))

    """
    Look for a pattern. Run 100 cycles, join all the rock rows into a single string, and look for a pattern.
    Start with the first, look for a match. Then add the index difference to the second and see if matches.
    Print the load after each cycle and look for a pattern.
    """

    """
    idx - pattern_start % pattern_length == pattern_idx
    pattern[p_start * p_length * (whatever)] = pattern[p_start]
    [87, 69, 69, 69, 65, 64, 65, 63, 68, 69, 69, 65, 64, 65, 63, 68, 69, 69, 65, 64, 65, 63, 68, 69, 69, 65, 64, 65, 63, 68, 69, 69, 65, 64, 65, 63, 68, 69, 69, 65, 64, 65, 63, 68, 69, 69, 65, 64, 65, 63]
    .....#.... 10
    ....#...O# 9
    ...OO##... 8
    .OO#...... 7
    .....OOO#. 6
    .O#...O#.# 5
    ....O#.... 4
    ......OOOO 3
    #...O###.. 2
    #..OO#.... 1
    """


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
