import re


def main():
    _map = {}
    with open("../inputs/day8_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            if "=" in line:
                mapping = re.findall(r"(\w\w\w) = \((\w\w\w), (\w\w\w)\)", line)[0]

                start, l, r = mapping[0], mapping[1], mapping[2]
                _map[start] = (l, r)

            elif len(line) > 1:
                instructions = line.replace("L", "0").replace("R", "1")

    steps = 0
    location = "AAA"
    while location != "ZZZ":
        for idx in instructions:
            move = int(idx)
            location = _map[location][move]
            steps += 1

    print(steps)


if __name__ == "__main__":
    main()
