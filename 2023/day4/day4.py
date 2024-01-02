import re


card_regex = re.compile("^Card \d+: (.*$)")


def main():
    debug = False
    total_points = 0

    with open("../inputs/day4_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            winning_nums, my_nums = line[10:].split("|")
            winning_nums = re.findall(r"(\d+)\s+", winning_nums)
            my_nums = re.findall(r"\s+(\d+)", my_nums)

            hits = list(set(winning_nums).intersection(my_nums))

            num_hits = len(hits)
            if num_hits:
                num_points = 2 ** (num_hits - 1)
                if debug:
                    print(f"Card {idx + 1} - {num_hits} hits - {num_points} points")
                total_points += num_points

    print(f"Total points: {total_points}")


if __name__ == "__main__":
    main()
