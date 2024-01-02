from collections import defaultdict
from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Garden:
    def __init__(self, plots, max_steps):
        self.plots = plots
        self.max_steps = max_steps
        self.starting_point = self.find_starting_point()
        self.reachable_points = set()
        # key: point, value: number of steps to reach point
        self.visited_points: dict[tuple[int, int], list[int]] = defaultdict(list)
        self.available_directions = None

    def walk(self):
        self.available_directions = Direction
        self.walk_from_point(self.starting_point, 1)

    def walk_from_point(self, point, cur_step):
        if cur_step > self.max_steps:
            return

        if point in self.visited_points and cur_step in self.visited_points[point]:
            return

        self.visited_points[point].append(cur_step)

        new_points = []
        for direction in self.available_directions:
            new_points.append(self.take_step(point, direction))

        new_reachable_points = [p[0] for p in new_points if p[1]]

        if cur_step % 2 == 0:
            self.reachable_points.update(new_reachable_points)

        for point in new_reachable_points:
            self.walk_from_point(point, cur_step + 1)

    def take_step(self, cur_point: tuple[int, int], direction: Direction):
        x = cur_point[0] + direction.value[0]
        y = cur_point[1] + direction.value[1]

        return (x, y), self.plots[y][x] != "#"

    def find_starting_point(self):
        for y, line in enumerate(self.plots):
            for x, char in enumerate(line):
                if char == "S":
                    return (x, y)

    def print_reachable_points(self):
        for y, line in enumerate(self.plots):
            for x, char in enumerate(line):
                if (x, y) == self.starting_point:
                    print("S", end="")
                elif (x, y) in self.reachable_points:
                    print("O", end="")
                else:
                    print(char, end="")
            print()

        print(f"Number of reachable points: {len(self.reachable_points)}")


def main():
    plots = []

    with open("../inputs/day21_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        plots = [line for line in read_data.splitlines()]

    garden = Garden(plots, 64)

    garden.walk()
    garden.print_reachable_points()


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
