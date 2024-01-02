import re

from shapely import Polygon


def main():
    dig_plan = []

    with open("../inputs/day18_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            direction, distance, color = re.search(
                r"(\w).(\d+).\(#(\w+)\)", line
            ).groups()

            dig_plan.append((direction, int(distance), color))

    lx, ly = (0, 0)
    vertices = [(lx, ly)]
    for step in dig_plan:
        match step[0]:
            case "U":
                dx, dy = (lx, ly - step[1])
            case "D":
                dx, dy = (lx, ly + step[1])
            case "L":
                dx, dy = (lx - step[1], ly)
            case "R":
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
