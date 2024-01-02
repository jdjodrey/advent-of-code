schematic = []


def check_left(x, y, print_part=False, cast_to_int=True):
    global schematic

    left = schematic[y][x - 1]

    if left.isdigit():
        all_left_digits = []
        while left.isdigit() and x > 0:
            x -= 1
            all_left_digits.append(str(left))
            left = schematic[y][x - 1]

        # flip cuz it's to the left
        all_left_digits.reverse()

        if print_part:
            print(f"Left part {''.join(all_left_digits)}")

        final_part = "".join(all_left_digits)
        return int(final_part) if cast_to_int else final_part
    else:
        return None


def check_right(x, y, print_part=False, cast_to_int=True):
    x = x + 1
    right = schematic[y][x]

    if right.isdigit():
        all_right_digits = []
        while right.isdigit() and x < 139:
            all_right_digits.append(str(right))
            x += 1
            right = schematic[y][x]

        if right.isdigit():
            all_right_digits.append(str(right))

        if print_part:
            print(f"Right part: {''.join(all_right_digits)}")

        final_part = "".join(all_right_digits)
        return int(final_part) if cast_to_int else final_part
    else:
        return None


def check_up(x, y):
    left_part = check_left(x, y - 1, print_part=False, cast_to_int=False)
    right_part = check_right(x, y - 1, print_part=False, cast_to_int=False)

    up = schematic[y - 1][x]
    if up.isdigit():
        all_up_digits = [up]
        if left_part is not None:
            all_up_digits.insert(0, left_part)
        if right_part is not None:
            all_up_digits.append(right_part)

        return int("".join([str(x) for x in all_up_digits])), 0
    else:
        if left_part is not None:
            left_part = int(left_part)
        if right_part is not None:
            right_part = int(right_part)
        return (left_part or 0), (right_part or 0)


def check_down(x, y):
    left_part = check_left(x, y + 1, print_part=False, cast_to_int=False)
    right_part = check_right(x, y + 1, print_part=False, cast_to_int=False)

    down = schematic[y + 1][x]

    if down.isdigit():
        all_down_digits = [down]
        if left_part is not None:
            all_down_digits.insert(0, left_part)
        if right_part is not None:
            all_down_digits.append(right_part)
        return int("".join([str(x) for x in all_down_digits])), 0
    else:
        if left_part is not None:
            left_part = int(left_part)
        if right_part is not None:
            right_part = int(right_part)
        return (left_part or 0), (right_part or 0)


def main():
    global schematic

    symbol_xy = []
    gear_ratios = []
    all_symbols = []

    with open("../inputs/day3_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        line_count = 0
        for line in read_data.splitlines():
            line = line.strip().replace(" ", "")
            schematic_line = []
            for idx, char in enumerate(line):
                schematic_line.append(char)
                if char == "*":
                    symbol_xy.append({"x": idx, "y": line_count})
                    all_symbols.append(char)
            schematic.append(schematic_line)
            line_count += 1

    debug = False
    for coord in symbol_xy:
        x = coord["x"]
        y = coord["y"]

        left_part = check_left(x, y) or 0
        right_part = check_right(x, y) or 0
        up_part1, up_part2 = check_up(x, y)
        down_part1, down_part2 = check_down(x, y)

        parts = [
            x
            for x in [left_part, right_part, up_part1, up_part2, down_part1, down_part2]
            if x > 0
        ]
        if len(parts) == 2:
            if debug:
                print(f"Gear found ({x}, {y+1}): {parts[0]}:{parts[1]}")
            gear_ratios.append(parts[0] * parts[1])

    print(f"Gear Ratio Sum: {sum(gear_ratios)}")


if __name__ == "__main__":
    main()
