def has_reflection(idx, pattern, offset=0):
    prev_idx = idx - offset
    next_idx = idx + offset + 1

    if prev_idx < 0 or next_idx == len(pattern):
        return True

    if pattern[prev_idx] == pattern[next_idx]:
        return has_reflection(idx, pattern, offset=offset + 1)

    return False


def main():
    patterns = []
    with open("../inputs/day13_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        pattern = []
        for line in read_data.splitlines():
            if line.strip() == "":
                patterns.append(pattern)
                pattern = []
                continue
            pattern.append(line)

        patterns.append(pattern)

    reflections = {
        "horizontal": [],
        "vertical": [],
    }

    for pattern in patterns:
        reflected = False
        # check for horizontal reflection
        for idx in range(len(pattern) - 1):
            if pattern[idx] == pattern[idx + 1]:
                if has_reflection(idx, pattern):
                    reflections["horizontal"].append(idx + 1)
                    reflected = True
                    break

        # check for vertical reflection
        if not reflected:
            pattern = list(zip(*reversed(pattern)))
            for idx in range(len(pattern) - 1):
                if pattern[idx] == pattern[idx + 1]:
                    if has_reflection(idx, pattern):
                        reflections["vertical"].append(idx + 1)
                        break

    sum_h = sum(reflections["horizontal"]) * 100
    sum_v = sum(reflections["vertical"])

    print(sum_h + sum_v)


if __name__ == "__main__":
    main()
