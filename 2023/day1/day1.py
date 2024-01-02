import re


def main():
    total = 0
    with open("../inputs/day1_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            str_digits = re.findall(r"\d", line)
            total += int(f"{str_digits[0]}{str_digits[-1]}")
    print(total)


if __name__ == "__main__":
    main()
