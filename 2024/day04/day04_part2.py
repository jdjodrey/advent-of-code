import time
from enum import IntEnum, Enum


class XmasEnum(IntEnum):
    X = 1
    M = 2
    A = 3
    S = 4


class TopCorners(Enum):
    NW = (-1, -1)
    NE = (1, -1)

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


def check_for_mas(x: int, y: int) -> bool:
    num_mas = 0
    for direction in TopCorners:
        next_x = x + direction.x
        next_y = y + direction.y

        try:
            corner = get_puzzle_value(next_x, next_y)

            opposite_corner_x = x + (direction.x * -1)
            opposite_corner_y = y + (direction.y * -1)

            is_mas = False
            if corner == XmasEnum.M:
                is_mas = (get_puzzle_value(opposite_corner_x, opposite_corner_y) == XmasEnum.S)

            elif corner == XmasEnum.S:
                is_mas = (get_puzzle_value(opposite_corner_x, opposite_corner_y) == XmasEnum.M)
        except IndexError:
            return False

        if is_mas:
            num_mas += 1

    return num_mas == 2


def main():
    global PUZZLE

    with open("../inputs/day04_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            PUZZLE.append([XmasEnum[x] for x in line])

    starting_pts: list[tuple[int, int]] = []
    for y, row in enumerate(PUZZLE):
        for x, value in enumerate(row):
            if value == XmasEnum.A:
                starting_pts.append((x, y))

    x_mas = []
    for x, y in starting_pts:
        if check_for_mas(x, y):
            x_mas.append((x, y))

    print(len(x_mas))


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
