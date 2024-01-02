import re


def hash_label(label):
    current_value = 0
    for char in label:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def print_boxes(step, boxes):
    print(f"\nAfter {step}:")
    for idx, box in enumerate(boxes):
        if len(box):
            print(f"Box {idx}: {box}")


def calc_focusing_power(boxes):
    """
    The focusing power of a single lens is the result of multiplying together:

    One plus the box number of the lens in question.
    The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    The focal length of the lens.
    """
    lens_focusing_power = []
    for box_num, box in enumerate(boxes):
        for slot_num, lens in enumerate(box):
            lens_focusing_power.append((box_num + 1) * (slot_num + 1) * lens[1])

    return sum(lens_focusing_power)


def main():
    steps = None
    with open("../inputs/day15_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        steps = read_data.splitlines()[0].split(",")

    boxes = [[] for _ in range(256)]
    for step in steps:
        label, op, focal_len = re.match(r"([a-z]+)([=-])(\d*)", step).groups()

        box_idx = hash_label(label)
        try:
            label_idx = [lens[0] for lens in boxes[box_idx]].index(label)
        except ValueError:
            label_idx = None

        if op == "=":
            lens = (label, int(focal_len))
            if label_idx is not None:
                boxes[box_idx][label_idx] = lens
            else:
                boxes[box_idx].append(lens)
        elif op == "-" and label_idx is not None:
            boxes[box_idx].pop(label_idx)

    print(f" Focusing power: {calc_focusing_power(boxes)}")


if __name__ == "__main__":
    main()
