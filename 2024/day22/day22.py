import math
import time


def mult_64(s: int) -> int:
    val = s * 64
    s = mix(s, val)
    return prune(s)


def div_32(s: int) -> int:
    val = math.floor(s / 32)
    s = mix(s, val)
    return prune(s)


def mult_2048(s: int) -> int:
    val = s * 2048
    s = mix(s, val)
    return prune(s)


def mix(s, val) -> int:
    """
    To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
    Then, the secret number becomes the result of that operation.
    (If the secret number is 42, and you were to mix 15 into the secret number, the secret number would become 37.)
    """
    return s ^ val


def prune(s) -> int:
    """
    To prune the secret number, calculate the value of the secret number modulo 16777216.
    Then, the secret number becomes the result of that operation.
    (If the secret number is 100000000, and you prune the secret number, the secret number would become 16113920.)
    """
    return s % 16777216


def next_secret_number(s: int) -> int:
    s = mult_64(s)
    s = div_32(s)
    return mult_2048(s)


def main():

    with open("../inputs/day22_input.txt", encoding="utf-8") as f:
        secret_nums = [int(s) for s in f.read().splitlines()]

    final_secret_nums = []
    for s in secret_nums:
        for _ in range(2000):
            s = next_secret_number(s)
            # print(s)
        final_secret_nums.append(s)

    print(sum(final_secret_nums))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")