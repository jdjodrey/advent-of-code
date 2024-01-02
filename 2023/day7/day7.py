from collections import Counter


card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def is_five_of_a_kind(hand):
    return len(set(hand)) == 1


def is_four_of_a_kind(hand):
    return len(set(hand)) == 2 and Counter(hand).most_common(1)[0][1] == 4


def is_full_house(hand):
    return len(set(hand)) == 2 and Counter(hand).most_common(1)[0][1] == 3


def is_three_of_a_kind(hand):
    return len(set(hand)) == 3 and Counter(hand).most_common(1)[0][1] == 3


def is_two_pair(hand):
    return len(set(hand)) == 3 and Counter(hand).most_common(1)[0][1] == 2


def is_one_pair(hand):
    return len(set(hand)) == 4


def determine_hand_rank(hand):
    if is_five_of_a_kind(hand):
        return 7
    elif is_four_of_a_kind(hand):
        return 6
    elif is_full_house(hand):
        return 5
    elif is_three_of_a_kind(hand):
        return 4
    elif is_two_pair(hand):
        return 3
    elif is_one_pair(hand):
        return 2
    return 1


def compare_same_rank_hands(hand1, hand2):
    for idx in range(len(hand1)):
        if card_ranks.index(hand1[idx]) > card_ranks.index(hand2[idx]):
            return True
        elif card_ranks.index(hand1[idx]) < card_ranks.index(hand2[idx]):
            return False
    return False


def main():
    hands = []
    with open("../inputs/day7_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            cards, bid = line.split(" ")
            hands.append(
                {"cards": cards, "bid": int(bid), "rank": determine_hand_rank(cards)}
            )

    hands = bubble_sort(hands)

    win_amounts = [h["bid"] * (idx + 1) for idx, h in enumerate(hands)]

    print(sum(win_amounts))


def bubble_sort(hands):
    for i in range(len(hands)):
        for j in range(0, len(hands) - i - 1):
            if hands[j]["rank"] > hands[j + 1]["rank"] or (
                hands[j]["rank"] == hands[j + 1]["rank"]
                and compare_same_rank_hands(hands[j]["cards"], hands[j + 1]["cards"])
            ):
                # swapping elements if elements
                # are not in the intended order
                temp = hands[j]
                hands[j] = hands[j + 1]
                hands[j + 1] = temp

    return hands


if __name__ == "__main__":
    main()
