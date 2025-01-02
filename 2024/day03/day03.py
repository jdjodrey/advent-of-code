import re
import time


def main():
    regex = r"mul\((\d{1,3}+),(\d{1,3}+)\)"

    with open("../inputs/day03_input.txt", encoding="utf-8") as f:
        memory = f.read()

    ops = re.findall(regex, memory)

    total = sum([int(x) * int(y) for x, y in ops])

    print(total)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
