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

    city_map: list[list[str]] = []

    with open("../inputs/day08_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for y, line in enumerate(read_data.splitlines()):
            city_map.append([x for x in line])
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

                # Add antennas positions
                anti_node_points.add(point1)
                anti_node_points.add(point2)

                # Ex. p1 = (5, 3) and p2 = (7, 7)
                # x_delta = -2, y_delta = -4
                # anti_node1 = (3, -1), anti_node2 = (9, 11)
                x_delta = point1.x - point2.x
                y_delta = point1.y - point2.y

                anti_node1_x = point1.x + x_delta
                anti_node1_y = point1.y + y_delta
                while 0 <= anti_node1_x <= max_x and 0 <= anti_node1_y <= max_y:
                    anti_node_points.add(Point(anti_node1_x, anti_node1_y))
                    anti_node1_x += x_delta
                    anti_node1_y += y_delta

                anti_node2_x = point2.x - x_delta
                anti_node2_y = point2.y - y_delta
                while 0 <= anti_node2_x <= max_x and 0 <= anti_node2_y <= max_y:
                    anti_node_points.add(Point(anti_node2_x, anti_node2_y))
                    anti_node2_x -= x_delta
                    anti_node2_y -= y_delta

    print(len(anti_node_points))


def print_anti_nodes(city_map, anti_node_points):
    for point in anti_node_points:
        city_map[point.y][point.x] = "#"

    for row in city_map:
        print("".join(row))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
