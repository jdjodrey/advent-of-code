import time
from copy import deepcopy
from enum import Enum


class Direction(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]

    def next_dir(self):
        # 90° clockwise rotation: (x,y) becomes (−y,x)
        next_x = -1 * self.y
        next_y = self.x
        return Direction((next_x, next_y))


def patrol(patrol_map, starting_loc) -> bool:
    guard_loc = starting_loc
    guard_dir = Direction.N

    visited_locs: set[tuple[tuple[int, int], Direction]] = set()
    while True:
        next_x = guard_loc[0] + guard_dir.x
        next_y = guard_loc[1] + guard_dir.y

        if next_y == len(patrol_map) or next_y < 0 or next_x == len(patrol_map[0]) or next_x < 0:
            break

        next_value = patrol_map[next_y][next_x]

        if next_value == "#":
            guard_dir = guard_dir.next_dir()
        else:
            next_loc = (next_x, next_y)

            if (next_loc, guard_dir) in visited_locs:
                return True

            guard_loc = next_loc
            visited_locs.add((guard_loc, guard_dir))


def main():
    patrol_map: list[list[str]] = []
    starting_loc: tuple[int, int] = (0, 0)

    with open("../inputs/day06_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            if "^" in line:
                starting_loc = (line.index("^"), idx)
            patrol_map.append([x for x in line])

    guard_loc = starting_loc
    guard_dir = Direction.N

    visited_locs: set[tuple[int, int]] = set()
    while True:
        next_x = guard_loc[0] + guard_dir.x
        next_y = guard_loc[1] + guard_dir.y

        if next_y == len(patrol_map) or next_y < 0 or next_x == len(patrol_map[0]) or next_x < 0:
            break

        next_value = patrol_map[next_y][next_x]

        if next_value == "#":
            guard_dir = guard_dir.next_dir()
        else:
            next_loc = (next_x, next_y)
            visited_locs.add(next_loc)
            guard_loc = next_loc
            patrol_map[next_y][next_x] = "X"

    obstacle_locs: set[tuple[int, int]] = set()
    for idx, loc in enumerate(visited_locs):
        if loc == starting_loc:
            continue

        local_map = deepcopy(patrol_map)
        local_map[loc[1]][loc[0]] = "#"

        if patrol(local_map, starting_loc):
            obstacle_locs.add(loc)

    print(len(obstacle_locs))


def print_map(patrol_map):
    for row in patrol_map:
        print(''.join(row))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
