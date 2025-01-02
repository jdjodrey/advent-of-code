import math
import re
import time
from collections import defaultdict


class SecretNum:
    def __init__(self, secret_num: int):
        self.secret_num: int = secret_num
        self.deltas: list[int] = []
        self.bananas: list[int] = []

        # Mapping of banana value to set of delta 4 sequences it occurs at
        # {7: set((1, 2, 6, -1), (-2, 1, -1, 3), ...)}
        self.delta_4s_by_banana: dict[int, set[tuple[int, ...]]] = defaultdict(set)

        # Mapping of the max banana associated with a delta 4 sequence
        # {(1, 2, 6, -1): 7, ...}
        self.max_bananas_by_delta_4: dict[tuple[int, ...], int] = defaultdict(int)

        # Mapping of the first banana associated with a delta 4 sequence
        # {(1, 2, 6, -1): 7, ...}
        self.first_bananas_by_delta_4: dict[tuple[int, ...], int] = {}

    def _mult_64(self):
        val = self.secret_num * 64
        self._mix(val)
        self._prune()

    def _div_32(self):
        val = math.floor(self.secret_num / 32)
        self._mix(val)
        self._prune()

    def _mult_2048(self):
        val = self.secret_num * 2048
        self._mix(val)
        self._prune()

    def _mix(self, val: int):
        """
        To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
        Then, the secret number becomes the result of that operation.
        (If the secret number is 42, and you were to mix 15 into the secret number, the secret number would become 37.)
        """
        self.secret_num = self.secret_num ^ val

    def _prune(self):
        """
        To prune the secret number, calculate the value of the secret number modulo 16777216.
        Then, the secret number becomes the result of that operation.
        (If the secret number is 100000000, and you prune the secret number, the secret number would become 16113920.)
        """
        self.secret_num = self.secret_num % 16777216

    def next_secret_number(self) -> int:
        self._mult_64()
        self._div_32()
        self._mult_2048()
        return self.secret_num

    def get_secret_nums(self):
        delta_4 = []

        for _ in range(2000):
            prev_s = self.secret_num
            next_s = self.next_secret_number()
            banana = next_s % 10
            delta = banana - (prev_s % 10)
            self.deltas.append(delta)
            self.bananas.append(banana)

            delta_4.append(delta)
            if len(delta_4) > 4:
                delta_4.pop(0)
            if len(delta_4) == 4:
                delta_4_tup = tuple(delta_4)
                self.delta_4s_by_banana[banana].add(delta_4_tup)
                # self.max_bananas_by_delta_4[tuple(delta_4)] = max(banana, self.max_bananas_by_delta_4[tuple(delta_4)])
                if delta_4_tup not in self.first_bananas_by_delta_4:
                    self.first_bananas_by_delta_4[delta_4_tup] = banana

        pass


def main():

    with open("../inputs/day22_input.txt", encoding="utf-8") as f:
        secret_nums: list[SecretNum] = [SecretNum(int(s)) for s in f.read().splitlines()]

    all_delta_4s = set()
    for S in secret_nums:
        S.get_secret_nums()
        all_delta_4s.update(set(S.first_bananas_by_delta_4.keys()))

    total_bananas_by_delta_4: dict[tuple[int, ...], int] = {}
    delta_4_by_total_bananas: dict[int, tuple[int, ...]] = {}

    for delta_4 in all_delta_4s:
        total_bananas = 0
        for S in secret_nums:
            total_bananas += S.first_bananas_by_delta_4.get(delta_4, 0)

        total_bananas_by_delta_4[delta_4] = total_bananas
        delta_4_by_total_bananas[total_bananas] = delta_4

    max_bananas = max(delta_4_by_total_bananas.keys())
    print(delta_4_by_total_bananas[max_bananas], max_bananas)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")