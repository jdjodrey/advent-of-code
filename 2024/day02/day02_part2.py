import time
from itertools import pairwise


def is_report_safe(report: list[int]) -> bool:
    if len(report) != len(set(report)):
        return False
    elif report != sorted(report) and report != sorted(report, reverse=True):
        return False
    else:
        max_gap = max([abs(x - y) for x, y in pairwise(report)])
        if max_gap > 3:
            return False

    return True


def main():
    reports = []
    with open("../inputs/day02_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            reports.append([int(num) for num in line.split()])

    num_unsafe = 0

    for report in reports:
        print(f"Checking {report}")
        is_safe = is_report_safe(report)
        if not is_safe:
            for idx in range(len(report)):
                report_copy = report.copy()
                report_copy.pop(idx)

                is_safe = is_report_safe(report_copy)
                if is_safe:
                    break

        if not is_safe:
            num_unsafe += 1
            continue

    print(f"Total reports: {len(reports)}")
    print(f"Safe reports: {len(reports) - num_unsafe}")
    print(f"Unsafe reports: {num_unsafe}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
