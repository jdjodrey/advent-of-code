import matplotlib as mpl
import matplotlib.path as mpl_path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Brick:
    def __init__(self, p1, p2, label):
        self.p1 = p1
        self.p2 = p2
        self.label = label
        self.is_vertical = p1[0] == p2[0] and p1[1] == p2[1]
        self.height = abs(p1[2] - p2[2])

        self.xy_points = self.get_all_xy_points()
        self.path = mpl_path.Path([(p1[0], p1[1]), (p2[0], p2[1])])

        # labels for bricks that this brick is supporting
        self.bricks_above: set(str) = set()

        # labels for bricks that are supporting this brick
        self.bricks_below: set(str) = set()

    def drop(self, new_z):
        if self.is_vertical:
            self.p2 = (self.p2[0], self.p2[1], self.p2[2] - (self.p1[2] - new_z))
            self.p1 = (self.p1[0], self.p1[1], new_z)
            self.height = abs(self.p1[2] - self.p2[2])

        else:
            self.p1 = (self.p1[0], self.p1[1], new_z)
            self.p2 = (self.p2[0], self.p2[1], new_z)

    def __repr__(self):
        return f"Brick(#{self.label}, {(self.p1, self.p2)})"

    def get_all_points(self):
        points = set()
        x_range = range(int(self.p1[0]), int(self.p2[0]) + 1)
        y_range = range(int(self.p1[1]), int(self.p2[1]) + 1)
        z_range = range(int(self.p1[2]), int(self.p2[2]) + 1)
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    points.add((x, y, z))
        return points

    def get_all_xy_points(self):
        points = set()
        x_range = range(int(self.p1[0]), int(self.p2[0]) + 1)
        y_range = range(int(self.p1[1]), int(self.p2[1]) + 1)
        for x in x_range:
            for y in y_range:
                points.add((x, y))
        return points


class Grid:
    def __init__(self, bricks):
        self.bricks = sorted(bricks, key=lambda b: min(b.p1[2], b.p2[2]))
        self.bricks_by_label = {b.label: b for b in self.bricks}

    def get_supporting_bricks(self, label):
        """bricks that the given brick supports (i.e. are on top of it)"""
        brick = self.bricks_by_label[label]
        return [
            self.bricks_by_label[label] for label in brick.is_supporting_brick_labels
        ]

    def get_supported_by_bricks(self, label):
        """bricks that support the given brick (i.e. are under it)"""
        brick = self.bricks_by_label[label]
        return [
            self.bricks_by_label[label] for label in brick.supported_by_brick_labels
        ]

    def turn_on_gravity(self, debug=False):
        for idx, brick in enumerate(self.bricks):
            if debug:
                print(f"Dropping brick #{brick.label}...")

            # check for collisions with lower bricks
            collisions = []
            if idx != 0:
                lower_bricks = self.bricks[:idx]
                collisions = self.get_collisions(brick, lower_bricks)

            if any(collisions):
                colliding_bricks = [b for b, c in zip(lower_bricks, collisions) if c]
                collision_point = max([b.p2[2] for b in colliding_bricks])

                top_colliding_bricks = [
                    b for b in colliding_bricks if b.p2[2] == collision_point
                ]
                brick.drop(collision_point + 1)
                self.update_supporting_bricks(brick, top_colliding_bricks)

            # if there aren't any, drop the brick to the ground
            else:
                brick.drop(1)

    def get_collisions(self, brick, lower_bricks):
        # only need to look at the xy points
        collides = [
            len(brick.xy_points.intersection(b.xy_points)) > 0 for b in lower_bricks
        ]

        return collides

    def update_supporting_bricks(self, brick, colliding_bricks):
        for b in colliding_bricks:
            b.bricks_above.add(brick.label)
            brick.bricks_below.add(b.label)

    def get_disintegration_targets(self):
        # a brick can be disintegrated if either:
        # A) it is not the only supporting brick for any other brick
        # B) it does not support any other bricks (i.e. it is at the top)

        invalid_target_labels = set(
            [list(b.bricks_below)[0] for b in self.bricks if len(b.bricks_below) == 1]
        )
        return [
            label
            for label in self.bricks_by_label
            if label not in invalid_target_labels
        ]

    def plot_bricks(self, num_bricks=25, reverse=False):
        mpl.rcParams["legend.fontsize"] = 10
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        bricks_to_plot = self.bricks if not reverse else reversed(self.bricks)
        for idx, b in enumerate(bricks_to_plot):
            if idx == num_bricks:
                break

            xs = [b.p1[0], b.p2[0]]
            ys = [b.p1[1], b.p2[1]]
            zs = [b.p1[2], b.p2[2]]
            ax.plot(xs, ys, zs, label=b.label)

        tick_spacing = 1
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        ax.zaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

        plt.show()


def main():
    bricks = []

    with open("../inputs/day22_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            p1, p2 = line.split("~")

            brick = Brick(
                tuple(int(p) for p in p1.split(",")),
                tuple(int(p) for p in p2.split(",")),
                str(idx + 1),
            )
            bricks.append(brick)

    grid = Grid(bricks)

    # grid.plot_bricks()
    grid.turn_on_gravity()
    bricks_to_blast = grid.get_disintegration_targets()

    print(f"Num disintegration targets: {len(bricks_to_blast)}")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
