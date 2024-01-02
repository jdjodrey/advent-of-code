from collections import Counter
from enum import IntEnum


card_ranks = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


class HandRank(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


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
    pre_joker_rank = HandRank.HIGH_CARD
    num_jokers = hand.count("J")

    if is_five_of_a_kind(hand):
        pre_joker_rank = HandRank.FIVE_OF_A_KIND
    elif is_four_of_a_kind(hand):
        pre_joker_rank = HandRank.FOUR_OF_A_KIND
    elif is_full_house(hand):
        pre_joker_rank = HandRank.FULL_HOUSE
    elif is_three_of_a_kind(hand):
        pre_joker_rank = HandRank.THREE_OF_A_KIND
    elif is_two_pair(hand):
        pre_joker_rank = HandRank.TWO_PAIR
    elif is_one_pair(hand):
        pre_joker_rank = HandRank.ONE_PAIR

    return adjust_hand_rank_for_jokers(pre_joker_rank, num_jokers)


def adjust_hand_rank_for_jokers(pre_joker_rank, num_jokers):
    match num_jokers:
        case 1:
            if pre_joker_rank == HandRank.FOUR_OF_A_KIND:
                return HandRank.FIVE_OF_A_KIND
            elif pre_joker_rank == HandRank.THREE_OF_A_KIND:
                return HandRank.FOUR_OF_A_KIND
            elif pre_joker_rank == HandRank.TWO_PAIR:
                return HandRank.FULL_HOUSE
            elif pre_joker_rank == HandRank.ONE_PAIR:
                return HandRank.THREE_OF_A_KIND
            else:
                return HandRank.ONE_PAIR
        case 2:
            if pre_joker_rank == HandRank.FULL_HOUSE:
                return HandRank.FIVE_OF_A_KIND
            elif pre_joker_rank == HandRank.TWO_PAIR:
                return HandRank.FOUR_OF_A_KIND
            else:
                return HandRank.THREE_OF_A_KIND
        case 3:
            if pre_joker_rank == HandRank.FULL_HOUSE:
                return HandRank.FIVE_OF_A_KIND
            else:
                return HandRank.FOUR_OF_A_KIND
        case 4:
            return HandRank.FIVE_OF_A_KIND
        case _:
            return pre_joker_rank


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
