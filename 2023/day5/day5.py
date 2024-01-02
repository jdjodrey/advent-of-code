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
                seeds = [{"types": [int(x)]} for x in re.findall(r"\s+(\d+)", line)]
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
        for seed in seeds:
            # seed = {"types": [x, ...]}
            type_num = seed["types"][-1]
            next_type_num = type_num
            for map_type, mappings in entries.items():
                for mapping in mappings:
                    dest = mapping[0]
                    src = mapping[1]
                    rng = mapping[2]
                    if src <= type_num <= src + rng:
                        next_type_num = dest + (type_num - src)
                        break

            seed["types"].append(next_type_num)

    print(f"Lowest location: {min([x['types'][-1] for x in seeds])}")


if __name__ == "__main__":
    main()
