def main():
    LINE_LEN = 140
    symbols = ["*", "#", "$", "%", "-", "@", "&", "=", "+", "/"]
    part_nums = []
    schematic_line = ""
    with open("../inputs/day3_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            line = line.strip().replace(" ", "")
            schematic_line += line

    idx = 0
    debug = False
    while idx < len(schematic_line):
        num = ""
        char = schematic_line[idx]
        while char.isdigit():
            num += char
            idx += 1
            char = schematic_line[idx]

        if num:
            # check left
            if schematic_line[idx - len(num) - 1] in symbols:
                if debug:
                    print(
                        f"Part {num} found RIGHT of {schematic_line[idx - len(num) - 1]}"
                    )
                part_nums.append(int(num))

            # check right
            elif schematic_line[idx] in symbols:
                if debug:
                    print(f"Part {num} found LEFT of {schematic_line[idx]}")
                part_nums.append(int(num))

            # check "up"
            elif not set(
                schematic_line[idx - LINE_LEN - len(num) - 1 : idx - LINE_LEN + 1]
            ).isdisjoint(set(symbols)):
                if debug:
                    print(
                        f"Part {num} found BELOW {schematic_line[idx - LINE_LEN - len(num) - 1 : idx - LINE_LEN + 1]}"
                    )
                part_nums.append(int(num))
            # check "down"
            elif not set(
                schematic_line[idx + LINE_LEN - len(num) - 1 : idx + LINE_LEN + 1]
            ).isdisjoint(set(symbols)):
                if debug:
                    print(
                        f"Part {num} found ABOVE {schematic_line[idx + LINE_LEN - len(num) - 1 : idx + LINE_LEN + 1]}"
                    )
                part_nums.append(int(num))

        idx += 1

    print(sum(part_nums))


if __name__ == "__main__":
    main()
