import time
from functools import lru_cache


@lru_cache(maxsize=None)
def blink(stone: int) -> tuple[int, int | None]:

    if stone == 0:
        return 1, None

    elif (stone_length := len(str(stone))) % 2 == 0:
        middle = stone_length//2
        left_stone = int(str(stone)[:middle])
        right_stone = int(str(stone)[middle:])
        return left_stone, right_stone

    else:
        return stone * 2024, None


@lru_cache(maxsize=None)
def count_blink_stones(stone: int, blinks_left: int) -> int:

    left_stone, right_stone = blink(stone)

    if blinks_left == 1:
        return 1 if right_stone is None else 2

    else:
        total = count_blink_stones(left_stone, blinks_left - 1)
        if right_stone is not None:
            total += count_blink_stones(right_stone, blinks_left - 1)
        return total


def main():

    with open("../inputs/day11_input.txt", encoding="utf-8") as f:
        starting_stones = [int(s) for s in str(f.read()).split()]

    times_to_blink = 75
    total_stones = 0
    for s in starting_stones:
        total_stones += count_blink_stones(s, times_to_blink)

    print(total_stones)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
