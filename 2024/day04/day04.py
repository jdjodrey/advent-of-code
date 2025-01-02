import time
from collections import defaultdict
from enum import IntEnum, Enum


class XmasEnum(IntEnum):
    X = 1
    M = 2
    A = 3
    S = 4


class Direction(Enum):
    W = (-1, 0)
    NW = (-1, -1)
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


PUZZLE: list[list[XmasEnum]] = []


def get_puzzle_value(x: int, y: int) -> XmasEnum:
    global PUZZLE
    if x < 0 or y < 0:
        raise IndexError

    return PUZZLE[y][x]


def check_spelling(value: XmasEnum, x: int, y: int, direction: Direction) -> bool:
    global PUZZLE

    next_x = x + direction.x
    next_y = y + direction.y

    try:
        next_value = get_puzzle_value(next_x, next_y)
    except IndexError:
        return False

    if value == XmasEnum.A and next_value == XmasEnum.S:
        return True

    if next_value - value == 1:
        return check_spelling(next_value, next_x, next_y, direction)

    return False


def main():
    global PUZZLE

    with open("../inputs//day04_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            PUZZLE.append([XmasEnum[x] for x in line])

    starting_pts: list[tuple[int, int]] = []
    for y, row in enumerate(PUZZLE):
        for x, value in enumerate(row):
            if value == XmasEnum.X:
                starting_pts.append((x, y))

    xmas = defaultdict(list)
    for x, y in starting_pts:
        for direction in Direction:
            if check_spelling(XmasEnum.X, x, y, direction):
                xmas[(x, y)].append(direction)

    total_xmas = sum([len(directions) for directions in xmas.values()])
    print(total_xmas)


def print_xmas(point, direction):
    global PUZZLE

    x = point[0]
    y = point[1]

    xmas = get_puzzle_value(x, y).name

    for _ in range(3):
        x += direction.x
        y += direction.y
        xmas += get_puzzle_value(x, y).name

    print(f"{point} -> Dir: {direction.name} -> {xmas}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
