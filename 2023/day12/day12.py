import re


def main():
    records = []
    with open("../inputs/day12_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            springs, groups = line.split()
            records.append(
                {
                    "springs": springs.strip("."),
                    "groups": [int(grp) for grp in groups.split(",")],
                    "num_configurations": 0,
                }
            )

    spring_mapping = {"1": "#", "0": "."}
    for rec in records:
        springs = rec["springs"]
        num_unknowns = springs.count("?")
        possibilities = 2**num_unknowns
        for num in range(possibilities):
            bin_str = bin(num)[2:].zfill(num_unknowns)

            for idx, j in enumerate(
                [m.start() for m in re.finditer(re.escape("?"), rec["springs"])]
            ):
                springs = springs[:j] + spring_mapping[bin_str[idx]] + springs[j + 1 :]

            spring_groups = [s for s in springs.split(".") if s.count("#") > 0]
            if len(spring_groups) != len(rec["groups"]):
                continue

            if all(
                [
                    len(spring_group) == grp
                    for spring_group, grp in zip(spring_groups, rec["groups"])
                ]
            ):
                rec["num_configurations"] += 1

    # print sum of all configurations
    print(sum([rec["num_configurations"] for rec in records]))


if __name__ == "__main__":
    main()
