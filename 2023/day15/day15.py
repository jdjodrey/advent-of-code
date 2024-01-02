def hash_char(current_value, char):
    current_value += ord(char)
    current_value *= 17
    current_value %= 256
    return current_value


def main():
    steps = []
    with open("../inputs/day15_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        steps = read_data.splitlines()[0].split(",")

    hashes = []

    for step in steps:
        current_value = 0
        for char in step:
            current_value = hash_char(current_value, char)

        hashes.append(current_value)

    print(f"Hash sum: {sum(hashes)}")


if __name__ == "__main__":
    main()
