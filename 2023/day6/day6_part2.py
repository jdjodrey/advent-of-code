import re


def main():
    time = 0
    distance = 0
    num_winning_distances = 0

    with open("../inputs/day6_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            num = "".join([x for x in re.findall(r"(\d+)", line)])
            print(line)
            if "Time" in line:
                time = int(num)
            else:
                distance = int(num)

    possible_distances = [(x * (time) - (x * x)) for x in range(0, time)]
    num_winning_distances = len([x for x in possible_distances if x > distance])
    print(num_winning_distances)


if __name__ == "__main__":
    main()
