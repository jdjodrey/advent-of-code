pipes = []


def get_next_pos(cur_pos, last_dir=None, check_for_start=True):
    global pipes

    up_pipes = ["|", "7", "F"]
    down_pipes = ["|", "L", "J"]
    left_pipes = ["-", "L", "F"]
    right_pipes = ["-", "J", "7"]

    if check_for_start:
        up_pipes.append("S")
        down_pipes.append("S")
        left_pipes.append("S")
        right_pipes.append("S")

    y, x = cur_pos
    up, down, left, right = ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))

    can_go_up = (
        y != 0
        and last_dir != "down"
        and pipes[up[0]][up[1]] in up_pipes
        and (not check_for_start or pipes[y][x] in down_pipes)
    )
    can_go_down = (
        y != len(pipes) - 1
        and last_dir != "up"
        and pipes[down[0]][down[1]] in down_pipes
        and (not check_for_start or pipes[y][x] in up_pipes)
    )
    can_go_left = (
        x != 0
        and last_dir != "right"
        and pipes[left[0]][left[1]] in left_pipes
        and (not check_for_start or pipes[y][x] in right_pipes)
    )
    can_go_right = (
        x != len(pipes[x]) - 1
        and last_dir != "left"
        and pipes[right[0]][right[1]] in right_pipes
        and (not check_for_start or pipes[y][x] in left_pipes)
    )

    if can_go_up:
        cur_pos, last_dir = up, "up"
    elif can_go_down:
        cur_pos, last_dir = down, "down"
    elif can_go_left:
        cur_pos, last_dir = left, "left"
    elif can_go_right:
        cur_pos, last_dir = right, "right"

    return cur_pos, last_dir


def main():
    global pipes
    start = None
    with open("../inputs/day10_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            pipes.append([x for x in line])
            if "S" in line:
                start = (idx, line.index("S"))

    cur_pos, last_dir = get_next_pos(start, check_for_start=False)

    pipe_len = 1
    while cur_pos != start:
        cur_pos, last_dir = get_next_pos(cur_pos, last_dir)
        pipe_len += 1

    print(f"pipe length: {pipe_len}")
    print(pipe_len // 2)


if __name__ == "__main__":
    main()
