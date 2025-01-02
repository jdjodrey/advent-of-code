import itertools
import re
import time


class Onsen:
    def __init__(self, towels: list[str], designs: list[str]):
        self.towels = towels
        self.designs = designs
        self.max_towel_size = max([len(t) for t in towels])

    def get_design_parts(self, design: str) -> list[str]:
        parts = [design[x:y] for x, y in itertools.combinations(range(len(design) + 1), r=2)]
        unique_possible_parts = []
        for p in parts:
            if len(p) <= self.max_towel_size and p not in unique_possible_parts:
                unique_possible_parts.append(p)
        return unique_possible_parts

    def num_designs_possible(self, design: str) -> int:
        parts = self.get_design_parts(design)
        # first_parts, rest_parts = parts[:self.max_towel_size], parts[self.max_towel_size:]

        # first_towels = list(set(self.towels).intersection(set(first_parts)))

        # matching_towels = list(set(self.towels).intersection(set(parts)))
        matching_towels = [t for t in parts if t in self.towels]
        matching_towels.sort(key=lambda t: len(t), reverse=True)

        stripe_re = re.compile(r"^(?:{})+$".format("|".join(matching_towels)))
        if not re.match(stripe_re, design):
            return 0

        stripe_re = re.compile(r"{}".format("|".join(matching_towels)))
        towel_stripes = re.findall(stripe_re, design)
        num_possible_design = 1
        for t in towel_stripes:
            if len(t) == 1:
                continue

            towel_pieces = [p for p in t if p in parts]
            num_possible_design += len(towel_pieces) - 1
            pass

        unique_towels = set(towel_stripes)
        unique_towel_combos = (
            set([tuple(set(x)) for x in itertools.combinations_with_replacement(unique_towels, r=len(unique_towels))])
        )
        pass
        for towels_to_remove in unique_towel_combos:
            towels_to_try = set(matching_towels) - set(towels_to_remove)
            if towels_to_try:
                stripe_re = re.compile(r"^(?:{})+$".format("|".join(towels_to_try)))
                if re.match(stripe_re, design):
                    num_designs_possible += 1

        print(design, num_designs_possible)
        return num_designs_possible

        # all_towel_stripes: set[tuple[str, ...]] = set()
        #
        # stripe_re = re.compile(r"{}".format("|".join([f"({t})*" for t in matching_towels])))
        # towel_stripes = re.findall(stripe_re, design)
        #
        # all_towel_stripes.add(tuple(towel_stripes))
        #
        # for towel in set(towel_stripes):
        #     matching_towels.pop(matching_towels.index(towel))
        #     stripe_re = re.compile(r"{}".format("|".join(matching_towels)))
        #     towel_stripes = re.findall(stripe_re, design)
        #     if "".join(towel_stripes) == design:
        #         all_towel_stripes.add(tuple(towel_stripes))
        #     matching_towels.append(towel)

        # for part_1 in first_parts:
        #
        #     # stripe_re = re.compile(f"({part_1})({'|'.join(matching_towels)})")
        #     towel_stripes = re.findall(stripe_re, design)
        #     towel_stripes = ["".join(stripe) for stripe in towel_stripes]
        #     if "".join(towel_stripes) == design:
        #         all_towel_stripes.add(tuple(towel_stripes))

        # for idx in range(len(matching_towels)):
        #     # matching_towels.pop()
        #     # if len("".join(matching_towels)) < len(design):
        #     #     break
        #
        #     stripe_re = re.compile('{}'.format("|".join(matching_towels)))
        #     towel_stripes = re.findall(stripe_re, design)
        #
        #     if "".join(towel_stripes) == design:
        #         all_towel_stripes.add(tuple(towel_stripes))
        #     matching_towels = matching_towels[1:] + matching_towels[:1]

        # print(design, len(all_towel_stripes), all_towel_stripes)
        # return len(all_towel_stripes)


def main():

    towels: list[str] = []
    designs: list[str] = []
    with open("../inputs/day19_input.txt", encoding="utf-8") as f:
        parse_designs = False
        for line in f.read().splitlines():
            if not line:
                parse_designs = True
                continue

            if parse_designs:
                designs.append(line)
            else:
                towels = [x.strip() for x in line.split(",")]

    o = Onsen(towels, designs)
    total_possible_designs = 0
    for idx, design in enumerate(o.designs):

        if num := o.num_designs_possible(design):
            total_possible_designs += num

    print(total_possible_designs)

    # 552 is too low
    # 7015 is too low
    # 8200 is too low
    # 15000 no feedback


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")