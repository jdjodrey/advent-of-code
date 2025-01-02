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
        return [p for p in parts if len(p) <= self.max_towel_size]

    def is_design_possible(self, design: str) -> bool:
        parts = self.get_design_parts(design)
        matching_towels = list(set(self.towels).intersection(set(parts)))

        stripe_re = re.compile(r"^(?:{})+$".format("|".join(matching_towels)))
        return bool(re.match(stripe_re, design))


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
    possible_designs: list[str] = []
    for idx, design in enumerate(o.designs):

        if o.is_design_possible(design):
            possible_designs.append(design)

    print(len(possible_designs))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")