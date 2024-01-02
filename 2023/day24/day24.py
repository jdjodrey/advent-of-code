from shapely.geometry import LineString, Point as ShapelyPoint


class ShapelyHail:
    def __init__(self, label, pos, vel):
        self.label = label
        self.p1 = ShapelyPoint(pos)

        # smallest velocity in input is 5, so scale up by 400000000000000 / 5
        # this ensures that the line will run outside of the target area
        self.p2 = ShapelyPoint(
            self.p1.x + (vel[0] * (400000000000000 / 5)),
            self.p1.y + (vel[1] * (400000000000000 / 5)),
        )

        self.line = LineString([self.p1, self.p2])


def main():
    hail_stones = []

    with open("../inputs/day24_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            pos, vel = line.split("@")
            hail_stones.append(
                ShapelyHail(
                    idx + 1,
                    [float(x) for x in pos.split(",")][:2],
                    [float(x) for x in vel.split(",")][:2],
                )
            )

    _max = 400000000000000
    _min = 200000000000000
    collision_points = []

    while len(hail_stones):
        hail = hail_stones.pop()

        num_collisions = 0
        num_bad_collisions = 0
        collision_labels = []
        for other_hail in hail_stones:
            if collision := hail.line.intersection(other_hail.line):
                if (_max >= collision.x >= _min) and (_max >= collision.y >= _min):
                    collision_points.append(collision)
                    num_collisions += 1
                    collision_labels.append(other_hail.label)
                else:
                    num_bad_collisions += 1

    print(f"Num collisions in target area: {len(collision_points)}")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
