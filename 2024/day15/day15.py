import time
from enum import StrEnum, Enum


class T(StrEnum):
    ROBOT = "@"
    WALL = "#"
    BOX = "O"
    EMPTY = "."


class Direction(Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


class Object:
    _TYPE: T | None = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self._TYPE}({self.x}, {self.y})"


class Robot(Object):
    _TYPE = T.ROBOT

    def move(self, direction: Direction):
        self.x += direction.x
        self.y += direction.y


class Wall(Object):
    _TYPE = T.WALL


class Box(Object):
    _TYPE = T.BOX

    def move(self, direction: Direction) -> tuple[int, int]:
        self.x += direction.x
        self.y += direction.y
        return self.x, self.y

    def gps(self):
        return (100 * self.y) + self.x


class Warehouse:
    def __init__(self, robot: Robot, boxes: list[Box], walls: list[Wall], layout: list[str], moves: str):
        self.robot = robot

        self.boxes = boxes
        self.boxes_by_pos: dict[tuple[int, int], Box] = {(b.x, b.y): b for b in self.boxes}

        self.walls = walls
        self.walls_by_pos: dict[tuple[int, int], Wall] = {(w.x, w.y): w for w in self.walls}

        self.layout = layout
        self.height = len(self.layout)
        self.width = len(self.layout[0])

        self.moves = moves

        self.direction_by_move = {
            "^": Direction.UP,
            ">": Direction.RIGHT,
            "<": Direction.LEFT,
            "v": Direction.DOWN
        }

    def move_robot(self, direction: Direction):
        next_pos = (self.robot.x + direction.x, self.robot.y + direction.y)

        if next_pos in self.walls_by_pos:
            pass

        elif next_pos in self.boxes_by_pos:
            pos = next_pos
            box_positions = []

            # Look in direction until we find either EMPTY or WALL
            while pos in self.boxes_by_pos:
                box_positions.append(pos)
                pos = (pos[0] + direction.x, pos[1] + direction.y)

            # If WALL, nothing moves
            if pos in self.walls_by_pos:
                pass

            # If EMPTY, move robot and all boxes in that direction
            else:
                self.robot.move(direction)

                # Process from the back so we don't overwrite the other box positions
                box_positions.reverse()
                for pos in box_positions:
                    box = self.boxes_by_pos.pop(pos)
                    new_box_pos = box.move(direction)
                    self.boxes_by_pos[new_box_pos] = box

        # Not a wall or box, so move robot
        else:
            self.robot.move(direction)

    def display(self):
        for y, row in enumerate(self.layout):
            line = ""
            for x, value in enumerate(row):
                pos = (x, y)
                if pos == (self.robot.x, self.robot.y):
                    line += T.ROBOT
                elif pos in self.boxes_by_pos:
                    line += T.BOX
                elif pos in self.walls_by_pos:
                    line += T.WALL
                else:
                    line += T.EMPTY
            print(line)


def main():

    robot: Robot | None = None
    walls: list[Wall] = []
    boxes: list[Box] = []
    layout: list[str] = []
    moves: str = ""
    with open("../inputs/day15_input.txt", encoding="utf-8") as f:

        parse_moves = False
        for y, line in enumerate(f.read().splitlines()):
            if line == "":
                parse_moves = True

            if parse_moves:
                moves += line
            else:
                layout.append(line)
                for x, value in enumerate(line):
                    if value == T.BOX:
                        boxes.append(Box(x, y))
                    elif value == T.WALL:
                        walls.append(Wall(x, y))
                    elif value == T.ROBOT:
                        robot = Robot(x, y)

    w = Warehouse(robot, boxes, walls, layout, moves)

    for move in w.moves:
        direction = w.direction_by_move[move]
        w.move_robot(direction)

    box_gps = sum([b.gps() for b in w.boxes])
    print(box_gps)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")