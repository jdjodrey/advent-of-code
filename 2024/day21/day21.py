import time
from enum import Enum


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


class Robot:
    def __init__(self, keypad: list[list[str]], _id: int):
        self.keypad = keypad
        self.pos = next((x, y) for y, row in enumerate(self.keypad) for x, button in enumerate(row) if button == "A")
        self._id = _id

    def __repr__(self):
        return f"R{self._id}({self.pos})='{self.keypad[self.pos[1]][self.pos[0]]}'"

    def move(self, pos: tuple[int, int]) -> str:
        moves = ""

        x_dist = pos[0] - self.pos[0]
        y_dist = pos[1] - self.pos[1]

        if x_dist < 0:
            move_x = self.pos[0] + (abs(x_dist) * Direction.LEFT.x)
            move_y = self.pos[1]
            if self.keypad[move_y][move_x] != " ":
                moves += abs(x_dist) * "<"
                self.pos = move_x, move_y
                x_dist = 0
        if x_dist > 0:
            moves += x_dist * ">"
            self.pos = self.pos[0] + (x_dist * Direction.RIGHT.x), self.pos[1]

        if y_dist < 0:
            moves += abs(y_dist) * "^"
            self.pos = self.pos[0], self.pos[1] + (abs(y_dist) * Direction.UP.y)
        if y_dist > 0:
            moves += y_dist * "v"
            self.pos = self.pos[0], self.pos[1] + (y_dist * Direction.DOWN.y)

        if x_dist < 0:
            moves += abs(x_dist) * "<"
            self.pos = self.pos[0] + (abs(x_dist) * Direction.LEFT.x), self.pos[1]
        # self.pos = self.pos[0] + d.x, self.pos[1] + d.y
        if self.keypad[self.pos[1]][self.pos[0]] == " ":
            print(f"Robot #{self._id} moved through gap!")

            # if d == Direction.LEFT:
            #     moves += "<"
            # elif d == Direction.RIGHT:
            #     moves += ">"
            # elif d == Direction.DOWN:
            #     moves += "v"
            # elif d == Direction.UP:
            #     moves += "^"

            # directions.sort(key=lambda d: (d.x, d.y), reverse=True)
            #
            # moves = ""
            # optimize_moves = True
            # while self.pos[0] != pos[0]:
            #
            #     if self.pos[1] != pos[1]:
            #         d = directions[0]
            #     elif len(directions) > 1:
            #         d = directions[1]
            #     else:
            #         d = directions[0]
            #
            #     if self.keypad[self.pos[1] + d.y][self.pos[0] + d.x] == " ":
            #         # print("Moved through gap!")
            #         optimize_moves = False
            #         d = next(d2 for d2 in directions if d2 != d)
            #
            #     self.pos = self.pos[0] + d.x, self.pos[1] + d.y
            #
            #     if d == Direction.LEFT:
            #         moves += "<"
            #     elif d == Direction.RIGHT:
            #         moves += ">"
            #     elif d == Direction.DOWN:
            #         moves += "v"
            #     elif d == Direction.UP:
            #         moves += "^"
            #
            # if optimize_moves:
            #     moves = "".join(sorted([x for x in moves]))
        return moves + "A"


def main():

    arrow_keypad = [
        [" ", "^", "A"],
        ["<", "v", ">"]
    ]
    number_keypad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [" ", "0", "A"]
    ]
    pos_by_number = {button: (x, y) for y, row in enumerate(number_keypad) for x, button in enumerate(row)}
    pos_by_arrow = {button: (x, y) for y, row in enumerate(arrow_keypad) for x, button in enumerate(row)}
    codes: list[list[str]] = []
    with open("../inputs/day21_input.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            codes.append([x for x in line])

    r1 = Robot(arrow_keypad, 1)
    r2 = Robot(arrow_keypad, 2)
    r3 = Robot(number_keypad, 3)

    all_moves_by_code = {}
    for code in codes:

        r3_moves = ""
        for digit in code:
            r3_moves += r3.move(pos_by_number[digit])
            # print(r3, r3_moves)

        r2_moves = ""
        for r2_arrow in r3_moves:
            r2_moves += r2.move(pos_by_arrow[r2_arrow])
            # print(r2, r2_moves, r2_arrow)

        r1_moves = ""
        for r1_arrow in r2_moves:
            r1_moves += r1.move(pos_by_arrow[r1_arrow])
            # code_moves += r1_moves
            # print(r1, r1_moves, r1_arrow)

        all_moves_by_code["".join(code)] = r1_moves

        print(r1_moves)
        print(r2_moves)
        print(r3_moves)
        print("".join(code))

    """
    <vA  <A   A  >>^A    vA  A   <^A >A      <v<A >>^A    vA  ^A      <vA   >^A     <v<A  >^A   >A      A       vA  ^A      <v<A    >A  >^A     A       A       vA      <^A     >A
    <v<A >A  <A  >>^A    vA  A   <^A >A      <v<A >>^A    vA  ^A      <vA   >^A     <v<A  >^A   >A      A       vA  ^A      <v<A    >A  >^A     A       A       vA      <^A     >A
    
    <    v   <   A       >   >   ^   A       <    A       >   A       v     A       <     ^     A       A       >   A       <       v   A       A       A       >       ^       A
    
    <                   A                   ^             A           >             ^                   ^       A           v                   v       v       A

    0   29A
    
    v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    <v<A>>^A<A>AvA<^AA>A<vAAA>^A
    
    379
    v<<A   >>^A  vA ^A  ||  v<<A >>^A A v<A   <A >>^A A    vA A  ^<A >A  || v<A >^A A <A >A v<A  <A >>^A A A vA ^<A >A 68
    <v<A   >>^A  vA ^A  ||  <vA  <A   A >>^A  A  vA   <^A  >A A  vA  ^A  || <vA >^A A <A >A <v<A >A >^A  A A vA <^A >A 64
    v<<A   >>^A  vA ^A      v<<A >>^A A v<A   <A >>^A A    vA A  ^<A >A v<A>^AA<A>Av<A<A>>^AAAvA^<A>A 379 68
    v<<A:   R1 presses "<"  R2 moves   "^"
    >^A:    R1 presses "A"  R2 presses "^"      R3 moves to 3
    vA:     R1 presses ">"  R2 moves   "A"
    ^A:     R1 presses "A"  R2 presses "A"      R3 presses 3
    
    THEIRS
    <vA:    R1 presses "v"  R2 moves   ">"
    <A:     R1 presses "<"  R2 moves   "v"
    A:      R1 presses "<"  R2 moves   "<"
    >>^A:   R1 presses "A"  R2 presses "<"      R3 moves to 2
    A:      R1 presses "A"  R2 presses "<"      R3 moves to 1
    vA:     R1 presses ">"  R2 moves   "v"
    <^A:    R1 presses "^"  R2 moves   "^"
    >A:     R1 presses "A"  R2 presses "^"      R3 moves to 4
    A:      R1 presses "A"  R2 presses "^"      R3 moves to 7
    vA:     R1 presses ">"  R2 moves   "A"
    ^A:     R1 presses "A"  R2 presses "A"      R3 presses 7
    
    MINE
    v<<A:   R1 presses "<"  R2 moves   "^"
    >>^A:   R1 presses "A"  R2 presses "^"      R3 moves to 6
    A:      R1 presses "A"  R2 presses "^"      R3 moves to 9
    v<A:    R1 presses "v"  R2 moves   "v"
    <A:     R1 presses "<"  R2 moves   "<"
    >>^A:   R1 presses "A"  R2 presses "<"      R3 moves to 8
    A:      R1 presses "A"  R2 presses "<"      R3 moves to 7
    vA:     R1 presses ">"  R2 moves   "v"
    A:      R1 presses ">"  R2 moves   ">"
    ^<A:    R1 presses "^"  R2 moves   "A"
    >A:     R1 presses "A"  R2 presses "A"      R3 presses 7
    """

    complexities = []
    for code, moves in all_moves_by_code.items():
        code_num = int(code[:-1])
        moves_num = len(moves)
        complexities.append(code_num * moves_num)
        print(code, moves, code_num, moves_num)

    print(sum(complexities))


# 179932 is too high
# 173472 is too high
# 172130 is not the right answer
# 171476 is not the right answer
# 170788 is too low

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")