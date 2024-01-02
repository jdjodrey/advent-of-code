import re


def main():
    seeds = []
    almanac = []
    map_type = ""
    current_map = None

    with open("../inputs/day5_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            if idx == 0:
                seed_pairs = re.findall(r"\s+(\d+)\s+(\d+)", line)
                # [('79', '14'), ('55', '13')]

                seeds = [
                    {"ranges": [range(int(pair[0]), int(pair[0]) + int(pair[1]))]}
                    for pair in seed_pairs
                ]

            elif "map" in line:
                map_type = re.findall(r"^(\w+-\w+-\w+)", line)[0]
                if current_map is not None:
                    almanac.append(current_map)

                current_map = {map_type: []}
            else:
                if (mapping := re.findall(r"\s*?(\d+)", line)) != []:
                    current_map[map_type].append(
                        (int(mapping[0]), int(mapping[1]), int(mapping[2]))
                    )
        almanac.append(current_map)

    for entries in almanac:
        for map_type, mappings in entries.items():
            for seed in seeds:
                type_range = seed["ranges"][-1]
                next_type_range = type_range
                for mapping in mappings:
                    dest_range = range(mapping[0], mapping[0] + mapping[2])
                    src_range = range(mapping[1], mapping[1] + mapping[2])

                    overlap = range(
                        max(type_range[0], src_range[0]),
                        min(type_range[-1], src_range[-1]) + 1,
                    )

                    if len(overlap):
                        next_type_range = range(
                            dest_range[0] + (overlap[0] - src_range[0]),
                            dest_range[0] + (overlap[-1] - src_range[0]) + 1,
                        )

                        break

                seed["ranges"].append(next_type_range)

    location_ranges = [x["ranges"][-1] for x in seeds]
    print(f"Lowest: {min([x[0] for x in location_ranges if len(x)])}")


if __name__ == "__main__":
    main()
