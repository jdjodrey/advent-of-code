import time
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


def main():

    guard_loc: tuple[int, int] = (0, 0)
    guard_dir: Direction = Direction.N
    patrol_map: list[list[str]] = []

    with open("../inputs/day06_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            if "^" in line:
                guard_loc = (line.index("^"), idx)
            patrol_map.append([x for x in line])

    visited_locs: set[tuple[int, int]] = {guard_loc}
    while True:
        next_x = guard_loc[0] + guard_dir.x
        next_y = guard_loc[1] + guard_dir.y

        try:
            next_value = patrol_map[next_y][next_x]
        except IndexError:
            break

        if next_value == "#":
            guard_dir = guard_dir.next_dir()
        else:
            next_loc = (next_x, next_y)
            visited_locs.add(next_loc)
            guard_loc = next_loc
            patrol_map[next_y][next_x] = "X"

    print(len(visited_locs))


def print_map(patrol_map, guard_loc, guard_dir):
    print(guard_loc, guard_dir)
    for row in patrol_map:
        print(''.join(row))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
