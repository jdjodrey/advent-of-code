import time
from collections import defaultdict
from copy import copy


# dict of all pages that must come before each page key
PAGE_ORDER: dict[int, list[int]] = defaultdict(list)


def check_order(update: list[int], was_reordered=False) -> bool:
    pages_to_print = copy(update)
    for idx, page in enumerate(pages_to_print):
        bad_pages = list(set(PAGE_ORDER[page]).intersection(set(pages_to_print[idx:])))
        if bad_pages:
            first_bad_page_idx = min([pages_to_print.index(x) for x in bad_pages])
            first_bad_page = pages_to_print[first_bad_page_idx]
            update.remove(first_bad_page)
            update.insert(idx, first_bad_page)
            return check_order(update, was_reordered=True)

    return was_reordered


def main():
    global PAGE_ORDER

    updates: list[list[int]] = []
    with open("../inputs/day05_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        lines = read_data.splitlines()

        while line := lines.pop(0):
            p1, p2 = (int(x) for x in line.split("|"))
            PAGE_ORDER[int(p2)].append(int(p1))

        for line in lines:
            updates.append([int(x) for x in line.split(",")])

    reordered_updates = []
    for update in updates:
        if check_order(update):
            reordered_updates.append(update)

    middle_sum = 0
    for update in reordered_updates:
        middle_idx = (len(update) - 1)//2
        middle_sum += update.pop(middle_idx)

    print(middle_sum)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")