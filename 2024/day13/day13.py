import re
import time


class Prize:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

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

        ax_moves: list[int] = []
        bx_moves: list[int] = []
        for i in range(1, 101):
            ax_move = i * self.a.x_move
            if ax_move <= self.prize.x:
                ax_moves.append(ax_move)

            bx_move = i * self.b.x_move
            if bx_move <= self.prize.x:
                bx_moves.append(bx_move)

        winning_plays: list[tuple[int, int]] = []
        for idx_a, ax in enumerate(ax_moves):
            for idx_b, bx in enumerate(bx_moves):
                if ax + bx == self.prize.x:
                    a_presses = idx_a + 1
                    b_presses = idx_b + 1
                    ay_move = a_presses * self.a.y_move
                    by_move = b_presses * self.b.y_move
                    if ay_move + by_move == self.prize.y:
                        winning_plays.append((a_presses, b_presses))
                elif ax + bx > self.prize.x:
                    break

        self.winning_plays = winning_plays

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