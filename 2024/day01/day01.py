import time


def main():
    entries = []
    with open("../inputs/day01_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            entries.append([int(num) for num in line.split()])

    left, right = [list(x) for x in zip(*entries)]
    left.sort()
    right.sort()

    total_distance = sum(
        [
            abs(left[idx] - right[idx])
            for idx in range(len(left))
        ]
    )

    print(total_distance)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
