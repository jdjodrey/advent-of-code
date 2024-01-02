import re
from enum import StrEnum

from shapely import Polygon


class Direction(StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


def get_dig_step_from_hex_color(hex_color):
    dir_map = {
        0: Direction.RIGHT,
        1: Direction.DOWN,
        2: Direction.LEFT,
        3: Direction.UP,
    }

    direction = dir_map[int(hex_color[-1:])]
    distance = int(hex_color[:-1], 16)

    return (direction, distance)


def main():
    dig_plan = []

    with open("../inputs/day18_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            color = re.search(r"#\w+", line).group()
            direction, distance = get_dig_step_from_hex_color(color[1:])
            dig_plan.append((direction, distance))

    lx, ly = (0, 0)
    vertices = [(lx, ly)]

    for step in dig_plan:
        match step[0]:
            case Direction.UP:
                dx, dy = (lx, ly - step[1])
            case Direction.DOWN:
                dx, dy = (lx, ly + step[1])
            case Direction.LEFT:
                dx, dy = (lx - step[1], ly)
            case Direction.RIGHT:
                dx, dy = (lx + step[1], ly)

        vertices.append((dx, dy))
        lx, ly = (dx, dy)

    pgon = Polygon(vertices)

    print(
        f"Dug area: {int(pgon.buffer(0.5, cap_style='square', join_style='mitre').area)}"
    )


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
