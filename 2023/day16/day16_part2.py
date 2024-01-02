from enum import StrEnum


class Direction(StrEnum):
    RIGHT = ">"
    LEFT = "<"
    UP = "^"
    DOWN = "v"


class Beam:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_redundant = False

    def move(self):
        if self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1
        elif self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1

    def as_vector(self):
        return (self.x, self.y, self.direction)

    def __repr__(self):
        return f"Beam(x={self.x}, y={self.y}, direction={self.direction})"

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.direction == other.direction
        )


class Grid:
    def __init__(self, tiles, starting_beam):
        self.height = len(tiles)
        self.width = len(tiles[0])
        self.tiles = tiles
        self.energized_tiles = set()
        self.beam_origins = set()
        self.beams = [starting_beam]

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def energize_tile(self, x, y):
        self.energized_tiles.add((x, y))

    def maybe_split_beam(self, beam, direction):
        if beam.as_vector() in self.beam_origins:
            beam.is_redundant = True
        else:
            self.beam_origins.add(beam.as_vector())

        # split beam if this is a new beam origin
        split_beam = Beam(x=beam.x, y=beam.y, direction=direction)
        if split_beam.as_vector() not in self.beam_origins:
            self.beams.append(split_beam)
            self.beam_origins.add(split_beam.as_vector())

    def move_beam(self, beam):
        beam.move()
        self.energize_tile(beam.x, beam.y)

        new_tile = self.get_tile(beam.x, beam.y)

        if new_tile == "-" and beam.direction in (Direction.UP, Direction.DOWN):
            beam.direction = Direction.LEFT
            self.maybe_split_beam(beam, Direction.RIGHT)

        elif new_tile == "|" and beam.direction in (Direction.LEFT, Direction.RIGHT):
            beam.direction = Direction.UP
            self.maybe_split_beam(beam, Direction.DOWN)

        elif new_tile == "/":
            match beam.direction:
                case Direction.RIGHT:
                    beam.direction = Direction.UP
                case Direction.LEFT:
                    beam.direction = Direction.DOWN
                case Direction.UP:
                    beam.direction = Direction.RIGHT
                case Direction.DOWN:
                    beam.direction = Direction.LEFT

        elif new_tile == "\\":
            match beam.direction:
                case Direction.RIGHT:
                    beam.direction = Direction.DOWN
                case Direction.LEFT:
                    beam.direction = Direction.UP
                case Direction.UP:
                    beam.direction = Direction.LEFT
                case Direction.DOWN:
                    beam.direction = Direction.RIGHT

    def display(self, show_energized_tiles=False):
        display_tiles = [list(line) for line in self.tiles]

        if show_energized_tiles:
            for tile in self.energized_tiles:
                display_tiles[tile[1]][tile[0]] = "#"
        for line in display_tiles:
            print("".join(line))

    def has_beam_ended(self, beam):
        """
        A beam has ended if it's pointing off the grid
        OR
        if it's going in the same direction as a previous beam
        """
        return (
            (beam.x == 0 and beam.direction == Direction.LEFT)
            or (beam.x == self.width - 1 and beam.direction == Direction.RIGHT)
            or (beam.y == 0 and beam.direction == Direction.UP)
            or (beam.y == self.height - 1 and beam.direction == Direction.DOWN)
            or beam.is_redundant
        )


def main():
    tiles = []
    with open("../inputs/day16_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            tiles.append(line)

    height = len(tiles)
    width = len(tiles[0])

    starting_beams = [
        Beam(x=-1, y=y, direction=Direction.RIGHT) for y in range(0, height)
    ]
    starting_beams += [
        Beam(x=x, y=-1, direction=Direction.DOWN) for x in range(0, width)
    ]
    starting_beams += [
        Beam(x=width, y=y, direction=Direction.LEFT) for y in range(0, height)
    ]
    starting_beams += [
        Beam(x=x, y=height, direction=Direction.UP) for x in range(0, width)
    ]

    max_num_energized_tiles = 0
    for beam in starting_beams:
        grid = Grid(tiles, beam)

        while len(grid.beams):
            beam = grid.beams.pop(0)
            while not grid.has_beam_ended(beam):
                grid.move_beam(beam)

        max_num_energized_tiles = max(
            max_num_energized_tiles, len(grid.energized_tiles)
        )

    # grid.display(show_energized_tiles=True)
    print(f"Max energized tiles: {max_num_energized_tiles}")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
