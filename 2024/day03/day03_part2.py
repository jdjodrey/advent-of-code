import re
import time


def main():
    regex = r"(mul\(\d{1,3}+,\d{1,3}+\))|(do\(\))|(don't\(\))"

    with open("../inputs/day03_input.txt", encoding="utf-8") as f:
        memory = f.read()

    ops = re.findall(regex, memory)

    total = 0
    enabled = True
    for op, do, dont in ops:
        if op and enabled:
            op = op.replace("mul(", "").replace(")", "").split(",")
            total += int(op[0]) * int(op[1])
        elif not op:
            enabled = do and not dont

    print(total)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
