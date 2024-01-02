def print_rocks(rocks):
    for idx, rock in enumerate(rocks):
        print("{0: <3}{1}".format(idx + 1, "".join(rock)))


def get_slide_index(idx, row):
    while idx + 1 < len(row) and row[idx + 1] == ".":
        idx += 1

    return idx


def calculate_load(rocks):
    load = 0
    for row in rocks:
        for idx in range(len(row)):
            if row[idx] == "O":
                load += idx + 1

    return load


def main():
    rocks = []
    with open("../inputs/day14_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            rocks.append([x for x in line])

    # rotate 90 degrees clockwise, so North (Up) is now East (Right)
    rocks = [list(x) for x in list(zip(*reversed(rocks)))]

    # iterate from the end of each row to the beginning
    for row in rocks:
        for idx in range(len(row) - 2, -1, -1):
            if row[idx] == "O" and (slide_index := get_slide_index(idx, row)):
                row[idx] = "."
                row[slide_index] = "O"

    load = calculate_load(rocks)
    print(f"Load: {load}")


if __name__ == "__main__":
    main()
