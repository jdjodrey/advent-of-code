import re


card_regex = re.compile("^Card \d+: (.*$)")


def main():
    cards = [1 for _ in range(1, 193)]

    debug = False
    with open("../inputs/day4_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            winning_nums, my_nums = line[10:].split("|")
            winning_nums = re.findall(r"(\d+)\s+", winning_nums)
            my_nums = re.findall(r"\s+(\d+)", my_nums)

            hits = list(set(winning_nums).intersection(my_nums))

            num_hits = len(hits)
            num_cards = cards[idx]

            if debug:
                print(f"Card #{idx + 1}: Copies: {num_cards} Hits: {num_hits}")

            for _ in range(0, num_cards):
                card_id = idx
                copies = num_hits
                while copies > 0:
                    card_id += 1
                    cards[card_id] += 1
                    copies -= 1

    print(f"Total cards: {sum(cards)}")


if __name__ == "__main__":
    main()
