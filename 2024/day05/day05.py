import time
from collections import defaultdict
from copy import copy


def main():
    # dict of all pages that must come before each page key
    page_order: dict[int, list[int]] = defaultdict(list)

    updates: list[list[int]] = []
    with open("../inputs/day05_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        lines = read_data.splitlines()

        while line := lines.pop(0):
            p1, p2 = (int(x) for x in line.split("|"))
            page_order[int(p2)].append(int(p1))

        for line in lines:
            updates.append([int(x) for x in line.split(",")])

    ordered_updates = []
    for update in updates:
        pages_to_print = copy(update)
        while len(pages_to_print):
            page = pages_to_print.pop(0)
            if set(page_order[page]).isdisjoint(set(pages_to_print)):
                if not len(pages_to_print):
                    ordered_updates.append(update)
            else:
                break

    middle_sum = 0
    for update in ordered_updates:
        middle_idx = (len(update) - 1)//2
        middle_sum += update.pop(middle_idx)

    print(middle_sum)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
