import time
from collections import Counter


def main():
    entries = []
    with open("../inputs/day01_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            entries.append([int(num) for num in line.split()])

    left, right = [list(x) for x in zip(*entries)]

    right_count = Counter(right)

    similarity_score = sum(num * right_count[num] for num in left)
    print(similarity_score)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
