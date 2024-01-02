import copy
from types import SimpleNamespace


pipes = []
pretty_pipes = []
pipe_pos = []


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
        x != len(pipes[0]) - 1
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


def prettify_pipes():
    global pipes
    global pipe_pos
    global pretty_pipes

    pretty_pipes = copy.deepcopy(pipes)
    for y, line in enumerate(pretty_pipes):
        for x, piece in enumerate(line):
            if (y, x) in pipe_pos:
                if piece == "7":
                    pretty_pipes[y][x] = "╮"
                elif piece == "J":
                    pretty_pipes[y][x] = "╯"
                elif piece == "F":
                    pretty_pipes[y][x] = "╭"
                elif piece == "L":
                    pretty_pipes[y][x] = "╰"
            else:
                pretty_pipes[y][x] = "."


def print_pipes(cur_pos=None, suspected_enclosed_pos=[], confirmed_enclosed_pos=[]):
    global pretty_pipes

    if suspected_enclosed_pos:
        for pos in suspected_enclosed_pos:
            pretty_pipes[pos[0]][pos[1]] = "O"

    if confirmed_enclosed_pos:
        for pos in confirmed_enclosed_pos:
            pretty_pipes[pos[0]][pos[1]] = "I"

    if cur_pos:
        tmp = pretty_pipes[cur_pos[0]][cur_pos[1]]
        pretty_pipes[cur_pos[0]][cur_pos[1]] = "@"

    print("    " + "".join([str(n) for n in range(len(pretty_pipes[0]))]))

    for idx, line in enumerate(pretty_pipes):
        prefix = "{0: >2}: ".format(idx)
        print(prefix + "".join(line))

    if cur_pos:
        pretty_pipes[cur_pos[0]][cur_pos[1]] = tmp


def main():
    global pipes
    global pipe_pos
    start = None

    with open("../inputs/day10_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for idx, line in enumerate(read_data.splitlines()):
            pipes.append([x for x in line])
            if "S" in line:
                start = (idx, line.index("S"))

    cur_pos, last_dir = get_next_pos(start, check_for_start=False)
    pipe_pos.append(cur_pos)

    pipe_len = 1
    while cur_pos != start:
        cur_pos, last_dir = get_next_pos(cur_pos, last_dir)

        pipe_pos.append(cur_pos)
        pipe_len += 1

    total_enclosed_pos = []
    for y, line in enumerate(pipes):
        inside_pipe = False
        prev_pos = None
        enclosed_pos = []
        for x, piece in enumerate(line):
            cur_pos = (y, x)

            if cur_pos not in pipe_pos and prev_pos in pipe_pos:
                enclosed_pos.append(cur_pos)
                inside_pipe = True
            elif cur_pos in pipe_pos and prev_pos not in pipe_pos:
                total_enclosed_pos += enclosed_pos
                enclosed_pos = []
                inside_pipe = False
            else:
                if inside_pipe:
                    enclosed_pos.append(cur_pos)

            prev_pos = cur_pos

    total_enclosed_pos2 = []
    for pos in total_enclosed_pos:
        y, x = pos

        if y == 0 or y == len(pipes) - 1:
            continue

        up_pos = (y - 1, x)
        while up_pos not in pipe_pos and up_pos[0] != 0:
            up_pos = (up_pos[0] - 1, up_pos[1])

        if up_pos[0] == 0:
            continue

        down_pos = (y + 1, x)
        while down_pos not in pipe_pos and down_pos[0] != len(pipes) - 1:
            down_pos = (down_pos[0] + 1, down_pos[1])

        if down_pos[0] == len(pipes) - 1:
            continue

        total_enclosed_pos2.append(pos)

    total_enclosed_pos = list(
        set(total_enclosed_pos).intersection(set(total_enclosed_pos2))
    )

    for pos in total_enclosed_pos:
        pipes[pos[0]][pos[1]] = "I"

    prettify_pipes()

    def can_reach_outside(
        pos, prev_pos, not_enclosed_pos, confirmed_enclosed_pos, debug=False, levels=0
    ):
        if pipes[pos[0]][pos[1]] == "I":
            debug = True
            print(f"{'-' * levels}inside pipe at {pos}")

        if debug:
            print(f"{'-' * levels}checking pos: {pos} prev pos: {prev_pos}")

        if pos in not_enclosed_pos:
            return True

        if pos in confirmed_enclosed_pos:
            return False

        y, x = pos
        directions = {
            "up": (y - 1, x),
            "down": (y + 1, x),
            "left": (y, x - 1),
            "right": (y, x + 1),
            "up_left": (y - 1, x - 1),
            "up_right": (y - 1, x + 1),
            "down_left": (y + 1, x - 1),
            "down_right": (y + 1, x + 1),
        }

        can_get_outside = True

        if debug:
            print(f"{'-' * levels}Looking up {pos}")
        if y == 0:
            can_get_outside = True
        elif (
            pipes[directions["up"][0]][directions["up"][1]] == "-"
            and directions["up"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["up"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["up"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside up: {can_get_outside}")
        if can_get_outside:
            return True
        if debug:
            print(f"{'-' * levels}Looking down {pos}")

        if y == len(pipes) - 1:
            can_get_outside = True
        elif (
            pipes[directions["down"][0]][directions["down"][1]] == "-"
            and directions["down"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["down"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["down"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside down: {can_get_outside}")
        if can_get_outside:
            return True
        if debug:
            print(f"{'-' * levels}Looking left {pos}")

        if x == 0:
            can_get_outside = True
        elif (
            pipes[directions["left"][0]][directions["left"][1]] == "|"
            and directions["left"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["left"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["left"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside left: {can_get_outside}")
        if can_get_outside:
            return True
        if debug:
            print(f"{'-' * levels}Looking right {pos}")

        if x == len(pipes[0]) - 1:
            can_get_outside = True
        elif (
            pipes[directions["right"][0]][directions["right"][1]] in ["|", "-"]
            and directions["right"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["right"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["right"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside right: {can_get_outside}")
        if can_get_outside:
            return True
        if debug:
            print(f"{'-' * levels}Looking up_left {pos}")

        if y == 0 or x == 0:
            can_get_outside = True
        elif (
            pipes[directions["up_left"][0]][directions["up_left"][1]] in ["F", "-"]
            and directions["up_left"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["up_left"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["up_left"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside up_left: {can_get_outside}")
        if can_get_outside:
            return True
        if debug:
            print(f"{'-' * levels}Looking up_right {pos}")

        if y == 0 or x == len(pipes[0]) - 1:
            can_get_outside = True
        elif (
            pipes[directions["up_right"][0]][directions["up_right"][1]] in ["7", "-"]
            and directions["up_right"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["up_right"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["up_right"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside up_right: {can_get_outside}")
        if can_get_outside:
            return True
        if debug:
            print(f"{'-' * levels}Looking down_left {pos}")

        if y == len(pipes) - 1 or x == 0:
            can_get_outside = True
        elif (
            pipes[directions["down_left"][0]][directions["down_left"][1]] in ["L", "-"]
            and directions["down_left"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["down_left"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["down_left"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside down_left: {can_get_outside}")
        if can_get_outside:
            return True
        if debug:
            print(f"{'-' * levels}Looking down_right {pos}")

        if y == len(pipes) - 1 or x == len(pipes[0]) - 1:
            can_get_outside = True
        elif (
            pipes[directions["down_right"][0]][directions["down_right"][1]]
            in ["J", "-"]
            and directions["down_right"] in pipe_pos
        ):
            can_get_outside = False
        elif directions["down_right"] != prev_pos:
            can_get_outside = can_reach_outside(
                directions["down_right"],
                pos,
                not_enclosed_pos,
                confirmed_enclosed_pos,
                debug=debug,
                levels=levels + 1,
            )

        if debug:
            print(f"{'-' * levels}can get outside down_right: {can_get_outside}")

        return can_get_outside

    def is_blocked_up(dir_chars):
        return (
            dir_chars[0] in ["F", "-"]
            and dir_chars[1] == "-"
            and dir_chars[2] in ["7", "-"]
        )

    def is_blocked_down(dir_chars):
        return (
            dir_chars[0] in ["L", "-"]
            and dir_chars[1] == "-"
            and dir_chars[2] in ["J", "-"]
        )

    def check_for_escape(
        cur_pos,
        prev_pos,
        not_enclosed_pos=[],
        confirmed_enclosed_pos=[],
        debug=False,
        levels=0,
    ):
        can_escape = False

        y, x = cur_pos
        directions = SimpleNamespace(
            up=[(y - 1, x - 1), (y - 1, x), (y - 1, x + 1)],
            down=[(y + 1, x - 1), (y + 1, x), (y + 1, x + 1)],
            # left=[(y, x - 1), (y - 1, x - 1), (y + 1, x - 1)],
            # right=[(y, x + 1), (y - 1, x + 1), (y + 1, x + 1)],
        )

        if cur_pos in not_enclosed_pos:
            return True

        if cur_pos in confirmed_enclosed_pos:
            return False

        for dir in directions.__dict__:
            dir_pos = getattr(directions, dir)
            dir_chars = [pipes[y][x] for y, x in dir_pos]

            if debug:
                print(
                    f"{'-' * levels}Looking {(dir.upper())} from {cur_pos} prev pos {prev_pos} chars: {dir_chars}"
                )
                print_pipes(cur_pos=cur_pos)

            # If we can ever get to the outside from this position, we can escape
            if any([c == "." for c in dir_chars]):
                if debug:
                    print(
                        f"{'-' * levels}ESCAPE! Can reach . from {cur_pos} going {dir}"
                    )
                return True

            # If we're not completely blocked, keep looking
            if any(
                [
                    (dir == "up" and not is_blocked_up(dir_chars)),
                    (dir == "down" and not is_blocked_down(dir_chars)),
                ]
            ):
                for n in range(3):
                    if getattr(directions, dir)[n] != prev_pos:
                        can_escape = check_for_escape(
                            getattr(directions, dir)[n],
                            cur_pos,
                            not_enclosed_pos,
                            confirmed_enclosed_pos,
                            debug=debug,
                            levels=levels + 1,
                        )
                        if can_escape:
                            break

            if debug:
                print(
                    f"{'-' * levels} Can escape = {can_escape} from {cur_pos} going {dir}"
                )

            return can_escape
        # can't go up if u/ul/ur are all F, -, 7
        # can't go down if d/dl/dr are all L, -, J

    def is_corner_pipe(pos):
        return pipes[pos[0]][pos[1]] in ["7", "J", "F", "L"]

    def get_next_pipe_pos(cur_pos):
        idx = pipe_pos.index(cur_pos)
        return pipe_pos[idx + 1] if idx + 1 < len(pipe_pos) else pipe_pos[0], cur_pos

    def get_next_check_direction(cur_pos, prev_pos, cur_check_dir):
        """
        symbol | move dir | check dir  | modifiers
        -------------------------------------------
        |      |     N    |   NW, SW   | (0, -1) {W}
        |      |     N    |   NE, SE   | (0, 1) {E}
        |      |     S    |   NW, SW   | (0, -1) {W}
        |      |     S    |   NE, SE   | (0, 1) {E}
        -      |     W    |   NW, NE   | (0, -1) {N}
        -      |     W    |   SW, SE   | (0, 1) {S}
        -      |     E    |   NW, NE   | (0, -1) {N}
        -      |     E    |   SW, SE   | (0, 1) {S}
        L      |     S    |   NW, SW   | [(0, 1), (-1, 0)] {SW}
        L      |     S    |   NE, SE   | [(0, -1), (1, 0)] {NE}
        L      |     W    |   NW, NE   | [(0, -1), (1, 0)] {NE}
        L      |     W    |   SW, SE   | [(0, 1), (-1, 0)] {SW}
        J      |     S    |   NW, SW   | [(0, -1), (-1, 0)] {NW}
        J      |     S    |   NE, SE   | [(0, 1), (1, 0)] {SE}
        J      |     E    |   NW, NE   | [(0, -1), (-1, 0)] {NW}
        J      |     E    |   SW, SE   | [(0, 1), (1, 0)] {SE}
        7      |     N    |   NW, SW   | [(0, 1), (-1, 0)] {SW}
        7      |     N    |   NE, SE   | [(0, -1), (1, 0)] {NE}
        7      |     E    |   NW, NE   | [(0, -1), (1, 0)] {NE}
        7      |     E    |   SW, SE   | [(0, 1), (-1, 0)] {SW}
        F      |     N    |   NW, SW   | [(0, -1), (-1, 0)] {NW}
        F      |     N    |   NE, SE   | [(0, 1), (1, 0)] {SE}
        F      |     W    |   NW, NE   | [(0, -1), (-1, 0)] {NW}
        F      |     W    |   SW, SE   | [(0, 1), (1, 0)] {SE}
        """

        """
        L rule
        S -> if has W, check SW, else check NE
        W -> if has N, check NE, else check SW
        """

        next_dir_map_by_piece = {
            "|": {
                "N": lambda d: "W" if "W" in d else "E",
                "S": lambda d: "W" if "W" in d else "E",
            },
            "-": {
                "W": lambda d: "N" if "N" in d else "S",
                "E": lambda d: "N" if "N" in d else "S",
            },
            "L": {
                "S": lambda d: "SW" if "W" in d else "NE",
                "W": lambda d: "NE" if "N" in d else "SW",
            },
            "J": {
                "S": lambda d: "NW" if "W" in d else "SE",
                "E": lambda d: "NW" if "N" in d else "SE",
            },
            "7": {
                "N": lambda d: "SW" if "W" in d else "NE",
                "E": lambda d: "NE" if "N" in d else "SW",
            },
            "F": {
                "N": lambda d: "NW" if "W" in d else "SE",
                "W": lambda d: "NW" if "N" in d else "SE",
            },
        }

        x_diff = cur_pos[1] - prev_pos[1]
        y_diff = cur_pos[0] - prev_pos[0]

        move_dir = None
        if x_diff == 1:
            move_dir = "E"
        elif x_diff == -1:
            move_dir = "W"
        elif y_diff == 1:
            move_dir = "S"
        elif y_diff == -1:
            move_dir = "N"
        else:
            raise Exception(f"Shouldn't hit this {cur_pos=} {prev_pos=}")

        piece = pipes[cur_pos[0]][cur_pos[1]]
        # print(f"{cur_pos=} {prev_pos=} {move_dir=} {piece=}")
        next_dir = next_dir_map_by_piece[piece][move_dir](cur_check_dir)
        return next_dir

    def get_modifiers_from_check_dir(check_dir):
        modifiers = []
        if "N" in check_dir:
            modifiers.append((-1, 0))
        if "S" in check_dir:
            modifiers.append((1, 0))
        if "W" in check_dir:
            modifiers.append((0, -1))
        if "E" in check_dir:
            modifiers.append((0, 1))

        return modifiers

    def is_outside(pos, not_enclosed_pos=[], confirmed_enclosed_pos=[], debug=False):
        # follow pipe all the way around or until you are on the same side as .

        search_pos = pos

        # go up until we hit a pipe
        while search_pos not in pipe_pos and search_pos[0] != 0:
            search_pos = (search_pos[0] - 1, search_pos[1])

        # if we never hit pipe, we're outside
        if search_pos not in pipe_pos:
            return True

        search_piece = pipes[search_pos[0]][search_pos[1]]
        # has to be one of -, L, J
        check_dir = "S"
        if search_piece == "L":
            check_dir = "SW"
        elif search_piece == "J":
            check_dir = "SE"

        if debug:
            print(
                f"START {pos=} piece {pipes[pos[0]][pos[1]]} found pipe at: {search_pos}"
            )

        cur_pos, prev_pos = get_next_pipe_pos(search_pos)

        while cur_pos != search_pos:
            check_dir = get_next_check_direction(cur_pos, prev_pos, check_dir)

            if debug:
                print(15 * "=")
                print(
                    f"{cur_pos=} {pipes[cur_pos[0]][cur_pos[1]]} {prev_pos=} {pipes[prev_pos[0]][prev_pos[1]]} {check_dir=}"
                )

            modifiers = get_modifiers_from_check_dir(check_dir)

            all_check_pos = [(cur_pos[0] + m[0], cur_pos[1] + m[1]) for m in modifiers]

            for check_pos in all_check_pos:
                # if we're checking off the map, we're outside
                if (
                    check_pos[0] < 0
                    or check_pos[0] >= len(pipes)
                    or check_pos[1] < 0
                    or check_pos[1] >= len(pipes[0])
                ):
                    if debug:
                        print(f"checking pos: {check_pos} is off the map!")

                    return True

                if debug:
                    print(
                        f"checking pos: {check_pos} piece {pipes[check_pos[0]][check_pos[1]]}"
                    )

                if pipes[check_pos[0]][check_pos[1]] == ".":
                    return True
                elif check_pos in not_enclosed_pos:
                    return True
                elif check_pos in confirmed_enclosed_pos:
                    return False

            cur_pos, prev_pos = get_next_pipe_pos(cur_pos)

        return False

    not_enclosed_pos = []
    confirmed_enclosed_pos = []
    prev_pos = None
    pipes[start[0]][start[1]] = "-"

    for pos in total_enclosed_pos:
        debug_pos = []
        # search for a pipe in every direction
        # stop if we reach the edge of the map or a pipe
        # if we reach the edge of the map, this pos is not enclosed
        if is_outside(
            pos, not_enclosed_pos, confirmed_enclosed_pos, debug=bool(pos in debug_pos)
        ):
            not_enclosed_pos.append(pos)
        else:
            confirmed_enclosed_pos.append(pos)

        prev_pos = pos

    print_pipes(
        suspected_enclosed_pos=total_enclosed_pos,
        confirmed_enclosed_pos=confirmed_enclosed_pos,
    )

    total_enclosed_pos = [
        pos for pos in total_enclosed_pos if pos not in not_enclosed_pos
    ]

    print(f"num total enclosed: {len(total_enclosed_pos)}")


if __name__ == "__main__":
    main()
