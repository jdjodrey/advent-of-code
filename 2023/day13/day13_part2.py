def has_reflection(idx, pattern, offset=0):
    prev_idx = idx - offset
    next_idx = idx + offset + 1

    if prev_idx < 0 or next_idx == len(pattern):
        return True

    if pattern[prev_idx] == pattern[next_idx]:
        return has_reflection(idx, pattern, offset=offset + 1)

    return False


def has_smudged_reflection(idx, pattern, offset=0, still_smudged=True):
    prev_idx = idx - offset
    next_idx = idx + offset + 1

    if idx == 0 or prev_idx < 0 or next_idx == len(pattern):
        return True

    if pattern[prev_idx] == pattern[next_idx]:
        return has_smudged_reflection(
            idx, pattern, offset=offset + 1, still_smudged=still_smudged
        )
    elif still_smudged and differs_by_one_bit(pattern[prev_idx], pattern[next_idx]):
        return has_smudged_reflection(
            idx, pattern, offset=offset + 1, still_smudged=False
        )

    return False


def convert_to_binary(line):
    trans_table = line.maketrans("#.", "10")
    return line.translate(trans_table)


def differs_by_one_bit(pattern1, pattern2):
    xor = int(pattern1, 2) ^ int(pattern2, 2)
    return xor and ((xor & (xor - 1)) == 0)


def print_patterns(patterns):
    for pattern in patterns:
        flipped = ["".join(x) for x in list(zip(*reversed(pattern["mirrors"])))]
        for idx in range(max(len(pattern["mirrors"]), len(flipped))):
            print(
                f"{pattern['mirrors'][idx] if idx < len(pattern['mirrors']) else ' ' * len(pattern['mirrors'][0])} | {flipped[idx] if idx < len(flipped) else ''}"
            )

        print(f'Orig: {pattern["orig_reflection"]} New: {pattern["new_reflection"]}')
        print(25 * "-")


def main():
    patterns = []

    with open("../inputs/day13_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        pattern = []
        for line in read_data.splitlines():
            if not len(line.strip()):
                patterns.append(
                    {
                        "mirrors": pattern,
                        "orig_reflection": None,
                        "new_reflection": None,
                    }
                )
                pattern = []
            else:
                pattern.append(convert_to_binary(line))

        patterns.append(
            (
                {
                    "mirrors": pattern,
                    "orig_reflection": None,
                    "new_reflection": None,
                }
            )
        )

    # find original reflections
    for pattern in patterns:
        mirrors = pattern["mirrors"]
        reflected = False
        # check for horizontal reflection
        for idx in range(len(mirrors) - 1):
            if mirrors[idx] == mirrors[idx + 1]:
                if has_reflection(idx, mirrors):
                    pattern["orig_reflection"] = (idx + 1, "h")
                    reflected = True
                    break

        # check for vertical reflection
        if not reflected:
            flipped_mirrors = ["".join(x) for x in list(zip(*reversed(mirrors)))]
            for idx in range(len(flipped_mirrors) - 1):
                if flipped_mirrors[idx] == flipped_mirrors[idx + 1]:
                    if has_reflection(idx, flipped_mirrors):
                        pattern["orig_reflection"] = (idx + 1, "v")
                        break

    orig_reflections = [p["orig_reflection"] for p in patterns]

    sum_h = sum([loc for loc, direction in orig_reflections if direction == "h"]) * 100
    sum_v = sum([loc for loc, direction in orig_reflections if direction == "v"])

    # find smudge and new reflections
    for pattern in patterns:
        mirrors = pattern["mirrors"]
        orig_r = pattern["orig_reflection"]
        reflected = False

        # check for horizontal reflection
        for idx in range(len(mirrors) - 1):
            # don't look in the same place for the reflection
            if orig_r[1] == "h" and idx + 1 == orig_r[0]:
                continue
            # breakpoint()
            if mirrors[idx] == mirrors[idx + 1]:
                if has_smudged_reflection(idx, mirrors):
                    pattern["new_reflection"] = (idx + 1, "h")
                    reflected = True
                    break
            # check if mirrors differ by a single bit (smudged)
            elif differs_by_one_bit(mirrors[idx], mirrors[idx + 1]):
                if has_smudged_reflection(idx, mirrors) and orig_r != (idx + 1, "h"):
                    pattern["new_reflection"] = (idx + 1, "h")
                    reflected = True
                    break

        # check for vertical reflection
        if not reflected:
            flipped_mirrors = ["".join(x) for x in list(zip(*reversed(mirrors)))]
            for idx in range(len(flipped_mirrors) - 1):
                # don't look in the same place for the reflection
                if orig_r[1] == "v" and idx + 1 == orig_r[0]:
                    continue

                if flipped_mirrors[idx] == flipped_mirrors[idx + 1]:
                    if has_smudged_reflection(idx, flipped_mirrors):
                        pattern["new_reflection"] = (idx + 1, "v")
                        reflected = True
                        break

                # check if mirrors differ by a single bit (smudged)
                elif differs_by_one_bit(flipped_mirrors[idx], flipped_mirrors[idx + 1]):
                    if has_smudged_reflection(idx, flipped_mirrors):
                        pattern["new_reflection"] = (idx + 1, "v")
                        reflected = True
                        break

    new_reflections = [p["new_reflection"] for p in patterns]

    sum_h = sum([loc for loc, direction in new_reflections if direction == "h"]) * 100
    sum_v = sum([loc for loc, direction in new_reflections if direction == "v"])
    print(sum_h + sum_v)


if __name__ == "__main__":
    main()
