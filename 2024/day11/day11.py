import time


def blink(stone: int, num: int) -> list[int]:
    """
    If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
        The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on
        the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is
        engraved on the new stone.
    """
    if num == 0:
        return [stone]

    if stone == 0:
        return blink(1, num - 1)
    elif (stone_length := len(str(stone))) % 2 == 0:
        middle = stone_length//2
        left_stone = int(str(stone)[:middle])
        right_stone = int(str(stone)[middle:])

        left_stones = blink(left_stone, num - 1)
        right_stones = blink(right_stone, num - 1)
        return [*left_stones, *right_stones]
    else:
        return blink(stone * 2024, num - 1)


def main():

    with open("../inputs/day11_input.txt", encoding="utf-8") as f:
        stones = [int(s) for s in str(f.read()).split()]

    num_stones = 0
    for stone in stones:
        stones = blink(stone, 25)
        num_stones += len(stones)

    print(num_stones)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
