import math
import re
import time


class Robot:
    def __init__(self, px: int, py: int, vx: int, vy: int):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

        self.max_x = 101
        self.max_y = 103

    def move(self, seconds: int):
        x_dis = seconds * self.vx
        y_dis = seconds * self.vy

        self.px = (self.px + x_dis) % self.max_x
        self.py = (self.py + y_dis) % self.max_y

    def get_quadrant(self) -> int:
        mid_x = (self.max_x - 1)//2
        mid_y = (self.max_y - 1)//2

        if self.px == mid_x or self.py == mid_y:
            return 0
        elif self.px < mid_x and self.py < mid_y:
            return 1
        elif self.px > mid_x and self.py < mid_y:
            return 2
        elif self.px < mid_x and self.py > mid_y:
            return 3
        elif self.px > mid_x and self.py > mid_y:
            return 4

    def __repr__(self):
        return f"R({self.px}, {self.py})"


def main():

    robot_re = r"p\=(-?\d+),(-?\d+) v\=(-?\d+),(-?\d+)"

    robots = []
    with open("../inputs/day14_input.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            px, py, vx, vy = [int(match) for match in re.findall(robot_re, line)[0]]
            robots.append(Robot(px, py, vx, vy))

    seconds = 100
    robots_in_quadrants = [0, 0, 0, 0]
    for robot in robots:
        robot.move(seconds)
        if quadrant := robot.get_quadrant():
            robots_in_quadrants[quadrant - 1] += 1

    print(math.prod(robots_in_quadrants))


def print_floor(robots: list[Robot]):
    width = robots[0].max_x
    height = robots[0].max_y

    floor = [[0] * width for _ in range(height)]
    for r in robots:
        floor[r.py][r.px] += 1

    for row in floor:
        print("".join([str(t) for t in row]).replace("0", "."))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")