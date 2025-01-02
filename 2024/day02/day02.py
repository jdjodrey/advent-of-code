import time
from itertools import pairwise


def main():
    reports = []
    with open("../inputs/day02_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            reports.append([int(num) for num in line.split()])

    num_unsafe = 0

    for report in reports:
        if len(report) != len(set(report)):
            num_unsafe += 1
        elif report != sorted(report) and report != sorted(report, reverse=True):
            num_unsafe += 1
        else:
            max_gap = max([abs(x - y) for x, y in pairwise(report)])
            if max_gap > 3:
                num_unsafe += 1

    print(f"Total reports: {len(reports)}")
    print(f"Safe reports: {len(reports) - num_unsafe}")
    print(f"Unsafe reports: {num_unsafe}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
