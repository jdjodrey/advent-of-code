from sympy import Line, Point, Ray


class HailStorm:
    def __init__(self, hail_stones):
        self.hail_stones = hail_stones
        self.cur_time = 0

    def advance_hail(self):
        for idx, hail in enumerate(self.hail_stones):
            if idx == 0:
                continue
            hail.loc.translate(*[x * (idx + self.cur_time) for x in hail.vel])


class Hail:
    def __init__(self, label, pos, vel):
        self.label = label
        self.orig = Point(pos)
        self.loc = Point(pos)
        self.vel = vel

    def location_at_time(self, time):
        return Point(
            self.orig.x + (self.vel[0] * time), self.orig.y + (self.vel[1] * time)
        )


def main():
    hail_stones = []

    with open("../inputs/day24_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            pos, vel = line.split("@")
            hail_stones.append(
                Hail(
                    idx + 1,
                    [float(x) for x in pos.split(",")],
                    [float(x) for x in vel.split(",")],
                )
            )

    storm = HailStorm(hail_stones)

    while True:
        storm.cur_time += 1
        for hail in storm.hail_stones:
            hail.loc = hail.location_at_time(storm.cur_time)
            for other_hail in storm.hail_stones:
                if hail.label == other_hail.label:
                    continue

                other_hail.loc = other_hail.location_at_time(storm.cur_time + 1)

        start = storm.hail_stones[0].loc
        # breakpoint()
        if start.is_collinear(*[hail.loc for hail in storm.hail_stones[1:]]):
            break
        # line = Line(storm.hail_stones[0].loc, storm.hail_stones[1].loc)
        # for hail in storm.hail_stones[2:]:
        #     if hail.loc not in line:
        #         break
        # else:
        #     break

        if storm.cur_time > 10:
            break

    print(f"Time: {storm.cur_time}")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
