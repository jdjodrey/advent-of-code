import time


def is_valid(total: int, factors: list[int]) -> bool:
    results = [factors.pop(0)]
    answers = []
    for num in factors:
        for r in results:
            answers.append(r + num)
            answers.append(r * num)
            answers.append(int(f"{r}{num}"))

        results = answers
        answers = []

    return total in results


def main():
    equations: dict[int, list[int]] = {}

    with open("../inputs/day07_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            parts = line.split(":")
            result = int(parts[0])
            factors = [int(x) for x in parts[1].strip().split()]
            equations[result] = factors

    valid_results = []

    for total, factors in equations.items():
        if is_valid(total, factors):
            valid_results.append(total)

    print(sum(valid_results))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")
