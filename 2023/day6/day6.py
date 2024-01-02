import re
from functools import reduce


def main():
    times = []
    distances = []
    num_winning_distances = []
    with open("../inputs/day6_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            nums = [int(x) for x in re.findall(r"(\d+)", line)]
            print(line)
            if "Time" in line:
                times = nums
            else:
                distances = nums

    for idx, time in enumerate(times):
        possible_distances = [(x * (time) - (x**2)) for x in range(0, time)]
        num_winning_distances.append(
            len([x for x in possible_distances if x > distances[idx]])
        )

    print(reduce(lambda x, y: x * y, num_winning_distances))


if __name__ == "__main__":
    main()
