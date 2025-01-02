import time


class Lock:
    def __init__(self, schematic):
        self.schematic = schematic
        rotated = list(zip(*schematic[::-1]))

        self.pin_depths = [c.count("#") - 1 for c in rotated]

    def __repr__(self):
        return f"Lock({self.pin_depths}"


class Key:
    def __init__(self, schematic):
        self.schematic = schematic
        rotated = list(zip(*schematic[::-1]))

        self.pin_depths = [c.count("#") - 1 for c in rotated]

    def __repr__(self):
        return f"Key({self.pin_depths}"


def main():

    locks = []
    keys = []

    with open("../inputs/day25_input.txt", encoding="utf-8") as f:
        schematic = []
        for line in f.read().splitlines():
            if not line:
                if schematic[0][0] == ".":
                    keys.append(schematic)
                else:
                    locks.append(schematic)
                schematic = []
            else:
                schematic.append(line)

        if schematic[0][0] == ".":
            keys.append(schematic)
        else:
            locks.append(schematic)

    locks = [Lock(l) for l in locks]
    keys = [Key(k) for k in keys]

    print(locks)
    print(keys)
    print(15 * "-")
    fits = 0
    height = 5
    for lock in locks:
        for key in keys:
            if all(lock.pin_depths[i] + key.pin_depths[i] <= height for i in range(height)):
                fits += 1

    print(fits)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")