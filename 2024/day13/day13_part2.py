import re
import time

from sympy import solve, Integer
from sympy.abc import x, y


class Prize:
    def __init__(self, x: int, y: int):
        self.x = x + 10000000000000
        self.y = y + 10000000000000

    def __repr__(self):
        return f"Node({self.x}, {self.y})"


class Button:
    def __init__(self, x_move: int, y_move: int):
        self.x_move = x_move
        self.y_move = y_move

    def __repr__(self):
        return f"Button(X+{self.x_move}, Y+{self.y_move})"


class Machine:
    def __init__(self, a: Button, b: Button, prize: Prize):
        self.a = a
        self.b = b
        self.prize = prize
        self.winning_plays: list[tuple[int, int]] = []

    def find_cheapest_win(self) -> int:
        if not len(self.winning_plays):
            return 0
        return min([(a * 3) + b for a, b in self.winning_plays])

    def play(self):
        # let x = the number of Button A presses
        # let y = the number of Button B presses

        # equation for x-axis
        eq1 = self.a.x_move * x + self.b.x_move * y - self.prize.x

        # equation for y-axis
        eq2 = self.a.y_move * x + self.b.y_move * y - self.prize.y

        winning_plays = solve([eq1, eq2], dict=True)
        for play in winning_plays:
            if isinstance(play[x], Integer) and isinstance(play[y], Integer):
                self.winning_plays.append((play[x], play[y]))

    def __repr__(self):
        return f"{self.a}, {self.b}, {self.prize}"


def main():
    button_re = r"Button \w: X\+(\d+), Y\+(\d+)"
    prize_re = r"Prize: X\=(\d+), Y\=(\d+)"

    machines = []
    with open("../inputs/day13_input.txt", encoding="utf-8") as f:
        lines = list(filter(lambda line: line != "", f.read().splitlines()))

        step = 3
        for idx in range(0, len(lines), step):
            a, b, prize = lines[idx:idx + step]

            ax, ay = [int(match) for match in re.findall(button_re, a)[0]]
            bx, by = [int(match) for match in re.findall(button_re, b)[0]]
            px, py = [int(match) for match in re.findall(prize_re, prize)[0]]

            machine = Machine(Button(ax, ay), Button(bx, by), Prize(px, py))
            machines.append(machine)

    tokens_needed = 0
    for m in machines:
        m.play()
        tokens_needed += m.find_cheapest_win()

    print(tokens_needed)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")