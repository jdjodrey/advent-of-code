from collections import defaultdict
from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Garden:
    def __init__(self, plots, max_steps):
        self.height = len(plots)
        self.width = len(plots[0])
        self.plots = plots
        self.max_steps = max_steps
        self.starting_point = self.find_starting_point()
        self.reachable_points = set()
        # key: point, value: number of steps to reach point
        self.visited_points: dict[tuple[int, int], list[int]] = defaultdict(list)

    def walk(self):
        self.walk_from_point(self.starting_point, 1)

    def walk_from_point(self, point, cur_step):
        if cur_step > self.max_steps:
            return

        if point in self.visited_points and cur_step in self.visited_points[point]:
            return

        self.visited_points[point].append(cur_step)

        new_points = []
        for direction in Direction:
            new_points.append(self.take_step(point, direction))

        new_reachable_points = [p[0] for p in new_points if p[1]]

        if cur_step % 2 == 0:
            self.reachable_points.update(new_reachable_points)

        for point in new_reachable_points:
            self.walk_from_point(point, cur_step + 1)

    def take_step(self, cur_point: tuple[int, int], direction: Direction):
        x = cur_point[0] + direction.value[0]
        y = cur_point[1] + direction.value[1]

        return (x, y), self.plots[y % self.height][x % self.width] != "#"

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

    def get_num_rocks(self):
        num_rocks = 0
        for line in self.plots:
            num_rocks += line.count("#")

        return num_rocks


"""
131 x 131
translate any point by 131 to get the same point
Need to calculate polygon area of the reachable points and subtract the number of rocks in the polygon


26501365 % 131 = 65
(26501365-65)/131 = 202300

11 x 11


P - S + 1 = 11?
16 - 6 + 1 = 11
50 - 10 + 1 = 41

40 rocks
81 plots


10 -> 50
12 -> 74
14 -> 99
16 -> 129
18 -> 165
20 -> 216
22 -> 261
24 -> 326
26 -> 395
28 -> 460
30 -> 537
32 -> 605
34 -> 689
36 -> 784
38 -> 894
40 -> 989
42 -> 1107
44 -> 1196
46 -> 1324
48 -> 1464

In exactly 6 steps, he can still reach 16 garden plots.
In exactly 10 steps, he can reach any of 50 garden plots.
In exactly 50 steps, he can reach 1594 garden plots.
In exactly 100 steps, he can reach 6536 garden plots.
In exactly 500 steps, he can reach 167004 garden plots.
In exactly 1000 steps, he can reach 668697 garden plots.
In exactly 5000 steps, he can reach 16733044 garden plots.

num_reachable = (0.75 * 17161 * (26501365^2))/14805

50 -> 2194
100 -> 8857
150 -> 19582


2356
14805
17161


40925293660
26501365

610565035183374 is too high
163701163660 is too low
40925293660 is too low

"""


def main():
    plots = []

    with open("../inputs/day21_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        plots = [line for line in read_data.splitlines()]

    garden = Garden(plots, 65)
    garden.walk()

    print(f"Reachable: {len(garden.reachable_points)}")
    print(f"Reachable Multiplied: {((202300 * 2) ** 2) + len(garden.reachable_points)}")

    print(f"{(131 * 131) - garden.get_num_rocks()}")

    # garden.walk()
    # garden.print_reachable_points()

    # 26501365 % 131 = 65


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
