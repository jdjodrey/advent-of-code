import time
from collections import defaultdict


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_out_of_bounds(self, max_x: int, max_y: int) -> bool:
        return min(self.x, self.y) < 0 or self.x > max_x or self.y > max_y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))


def main():
    points: list[Point] = []
    points_by_freq: dict[str, list[Point]] = defaultdict(list)

    with open("../inputs/day08_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for y, line in enumerate(read_data.splitlines()):
            for x, value in enumerate(line):
                if value != ".":
                    point = Point(x, y)
                    points.append(point)
                    points_by_freq[value].append(point)

        max_y = y
        max_x = x

    anti_node_points: set[Point] = set()
    for freq, points in points_by_freq.items():
        for idx1, point1 in enumerate(points):
            for idx2, point2 in enumerate(points):
                if point1 == point2:
                    continue

                # Ex. p1 = (5, 3) and p2 = (7, 7)
                # x_delta = -2, y_delta = -4
                # anti_node1 = (3, -1), anti_node2 = (9, 11)
                x_delta = point1.x - point2.x
                y_delta = point1.y - point2.y

                anti_node1 = Point(point1.x + x_delta, point1.y + y_delta)
                anti_node2 = Point(point2.x - x_delta, point2.y - y_delta)

                if not anti_node1.is_out_of_bounds(max_x, max_y):
                    anti_node_points.add(anti_node1)
                if not anti_node2.is_out_of_bounds(max_x, max_y):
                    anti_node_points.add(anti_node2)

    print(len(anti_node_points))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
