import regex as re


word_to_int = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def main():
    total = 0
    with open("../inputs/day1_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            str_digits = re.findall(
                r"\d|" + "|".join(list(word_to_int.keys())), line, overlapped=True
            )
            first_digit = (
                int(str_digits[0])
                if str_digits[0].isdigit()
                else word_to_int[str_digits[0]]
            )
            last_digit = (
                int(str_digits[-1])
                if str_digits[-1].isdigit()
                else word_to_int[str_digits[-1]]
            )

            total += int(f"{first_digit}{last_digit}")

    print(total)


if __name__ == "__main__":
    main()
