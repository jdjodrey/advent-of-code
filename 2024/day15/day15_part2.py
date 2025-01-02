import time
from enum import StrEnum, Enum


class T(StrEnum):
    ROBOT = "@"
    WALL = "#"
    BOX_L = "["
    BOX_R = "]"
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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self._TYPE == other._TYPE

    def __hash__(self):
        return hash(str(self))

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
    _TYPE = f"{T.BOX_L}{T.BOX_R}"

    def move(self, direction: Direction) -> tuple[int, int]:
        self.x += direction.x
        self.y += direction.y
        return self.x, self.y

    def gps(self):
        return (100 * self.y) + self.x


class Warehouse:
    def __init__(self, layout: list[str], moves: str):
        self.robot: Robot | None = None

        self.boxes: list[Box] = []
        self.left_boxes_by_pos: dict[tuple[int, int], Box] = {}
        self.right_boxes_by_pos: dict[tuple[int, int], Box] = {}

        self.walls: list[Wall] = []
        self.walls_by_pos: dict[tuple[int, int], Wall] = {}

        self.layout = layout

        self.moves = moves

        self.direction_by_move = {
            "^": Direction.UP,
            ">": Direction.RIGHT,
            "<": Direction.LEFT,
            "v": Direction.DOWN
        }

    def map_layout(self):
        for y, row in enumerate(self.layout):
            for x in range(0, len(row), 2):
                pos = (x, y)
                block = row[x:x + 2]
                if block == "[]":
                    box = Box(*pos)
                    self.boxes.append(box)
                    self.left_boxes_by_pos[pos] = box
                    self.right_boxes_by_pos[(x + 1, y)] = box
                elif block == "##":
                    wall = Wall(*pos)
                    self.walls.append(wall)
                    self.walls_by_pos[pos] = wall
                    self.walls_by_pos[(x + 1, y)] = wall
                elif T.ROBOT in block:
                    x = x if block[0] == T.ROBOT else x + 1
                    self.robot = Robot(x, y)

    def move_box_up_down(self, next_pos, direction, boxes_to_move) -> tuple[bool, list[Box]]:
        pos_l = (next_pos[0] + direction.x, next_pos[1] + direction.y)
        pos_r = (pos_l[0] + 1, pos_l[1])

        if pos_l in self.walls_by_pos or pos_r in self.walls_by_pos:
            return False, []
        elif pos_l in self.left_boxes_by_pos:
            boxes_to_move.append(self.left_boxes_by_pos[pos_l])
            return self.move_box_up_down(pos_l, direction, boxes_to_move)
        elif pos_l in self.right_boxes_by_pos and pos_r in self.left_boxes_by_pos:
            boxes_to_move.append(self.right_boxes_by_pos[pos_l])
            can_move, boxes_to_move = self.move_box_up_down((pos_l[0] - 1, pos_l[1]), direction, boxes_to_move)

            if not can_move:
                return False, []

            boxes_to_move.append(self.left_boxes_by_pos[pos_r])
            return self.move_box_up_down(pos_r, direction, boxes_to_move)
        elif pos_l in self.right_boxes_by_pos:
            boxes_to_move.append(self.right_boxes_by_pos[pos_l])
            return self.move_box_up_down((pos_l[0] - 1, pos_l[1]), direction, boxes_to_move)
        elif pos_r in self.left_boxes_by_pos:
            boxes_to_move.append(self.left_boxes_by_pos[pos_r])
            return self.move_box_up_down(pos_r, direction, boxes_to_move)

        return True, boxes_to_move

    def move_robot(self, direction: Direction):
        next_pos = (self.robot.x + direction.x, self.robot.y + direction.y)

        if next_pos in self.walls_by_pos:
            pass

        elif next_pos in self.left_boxes_by_pos:
            if direction == Direction.RIGHT:
                pos = next_pos
                left_box_positions = []

                # Look RIGHT two tiles at a time until we find either EMPTY or WALL
                while pos in self.left_boxes_by_pos:
                    left_box_positions.append(pos)
                    pos = (pos[0] + direction.x + 1, pos[1] + direction.y)

                # If WALL, nothing moves
                if pos in self.walls_by_pos:
                    pass

                # If EMPTY, move robot and all boxes in that direction
                else:
                    self.robot.move(direction)

                    # Process from the back so that we don't overwrite the other box positions
                    left_box_positions.reverse()
                    for pos in left_box_positions:
                        box = self.left_boxes_by_pos.pop(pos)
                        del self.right_boxes_by_pos[(box.x + 1, box.y)]
                        new_left_pos = box.move(direction)
                        self.left_boxes_by_pos[new_left_pos] = box
                        self.right_boxes_by_pos[(box.x + 1, box.y)] = box

            elif direction == Direction.LEFT:
                raise ValueError("Somehow hit the left side of a box while traveling left")

            # Going up/down, need to account for double push width
            else:
                box_to_move = self.left_boxes_by_pos[next_pos]
                can_move, boxes_to_move = self.move_box_up_down(next_pos, direction, [box_to_move])
                if can_move:
                    self.robot.move(direction)

                    boxes_to_move = set(boxes_to_move)
                    for box in boxes_to_move:
                        try:
                            del self.left_boxes_by_pos[(box.x, box.y)]
                            del self.right_boxes_by_pos[(box.x + 1, box.y)]
                        except KeyError:
                            pass
                        box.move(direction)

                    for box in boxes_to_move:
                        self.left_boxes_by_pos[(box.x, box.y)] = box
                        self.right_boxes_by_pos[(box.x + 1, box.y)] = box

        elif next_pos in self.right_boxes_by_pos:
            if direction == Direction.LEFT:
                pos = next_pos
                right_box_positions = []

                # Look LEFT two tiles at a time until we find either EMPTY or WALL
                while pos in self.right_boxes_by_pos:
                    right_box_positions.append(pos)
                    pos = (pos[0] + direction.x - 1, pos[1] + direction.y)

                # If WALL, nothing moves
                if pos in self.walls_by_pos:
                    pass

                # If EMPTY, move robot and all boxes in that direction
                else:
                    self.robot.move(direction)

                    # Process from the back so that we don't overwrite the other box positions
                    right_box_positions.reverse()
                    for pos in right_box_positions:
                        box = self.right_boxes_by_pos.pop(pos)
                        del self.left_boxes_by_pos[(box.x, box.y)]
                        new_left_pos = box.move(direction)
                        self.left_boxes_by_pos[new_left_pos] = box
                        self.right_boxes_by_pos[(box.x + 1, box.y)] = box

            elif direction == Direction.RIGHT:
                raise ValueError("Somehow hit the right side of a box while traveling right")

            # Going up/down, need to account for double push width
            else:
                box = self.right_boxes_by_pos[next_pos]
                next_pos = (next_pos[0] - 1, next_pos[1])
                can_move, boxes_to_move = self.move_box_up_down(next_pos, direction, [box])
                if can_move:
                    self.robot.move(direction)

                    boxes_to_move = set(boxes_to_move)
                    for box in boxes_to_move:
                        del self.left_boxes_by_pos[(box.x, box.y)]
                        del self.right_boxes_by_pos[(box.x + 1, box.y)]
                        box.move(direction)

                    for box in boxes_to_move:
                        self.left_boxes_by_pos[(box.x, box.y)] = box
                        self.right_boxes_by_pos[(box.x + 1, box.y)] = box

        # Not a wall or box, so move robot
        else:
            self.robot.move(direction)

        if set(self.walls_by_pos).intersection(self.right_boxes_by_pos):
            pass

    def display(self):
        for y, row in enumerate(self.layout):
            line = ""
            for x, value in enumerate(row):
                pos = (x, y)
                if pos == (self.robot.x, self.robot.y):
                    line += T.ROBOT
                elif pos in self.left_boxes_by_pos:
                    line += T.BOX_L
                elif pos in self.right_boxes_by_pos:
                    line += T.BOX_R
                elif pos in self.walls_by_pos:
                    line += T.WALL
                else:
                    line += T.EMPTY
            print(line)


def main():

    layout: list[str] = []
    moves: str = ""
    with open("../inputs/day15_input.txt", encoding="utf-8") as f:

        parse_moves = False
        for line in f.read().splitlines():
            if line == "":
                parse_moves = True

            if parse_moves:
                moves += line
            else:
                wider_line = line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
                layout.append(wider_line)

    w = Warehouse(layout, moves)
    w.map_layout()

    for move in w.moves:
        direction = w.direction_by_move[move]
        w.move_robot(direction)

    box_gps = sum([b.gps() for b in w.boxes])
    print(box_gps)


# 1437181 is too high
# 1429299

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")