import re

MAX_BLUES = 14
MAX_GREENS = 13
MAX_REDS = 12

game_id_regex = re.compile("Game (\d+): (.*$)")
pull_regex = re.compile("(\d+) (blue|green|red)")

game_ids = [x for x in range(1, 101)]
impossible_game_ids = []


def check_if_game_is_impossible(game_id, pull, debug=False):
    cubes = pull.split(", ")
    for cube in cubes:
        cube_match = pull_regex.match(cube)
        num = cube_match.group(1) if cube_match else 0
        color = cube_match.group(2) if cube_match else None

        if color == "blue" and int(num) > MAX_BLUES:
            if debug:
                print(f"Game {game_id} is impossible -> {cube} > {MAX_BLUES}")
            return True
        elif color == "green" and int(num) > MAX_GREENS:
            if debug:
                print(f"Game {game_id} is impossible -> {cube} > {MAX_GREENS}")
            return True
        elif color == "red" and int(num) > MAX_REDS:
            if debug:
                print(f"Game {game_id} is impossible -> {cube} > {MAX_REDS}")
            return True


def main():
    with open("../inputs/day2_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            game_id = game_id_regex.match(line).group(1)
            pulls = game_id_regex.match(line).group(2)
            for pull in pulls.split("; "):
                is_impossible = check_if_game_is_impossible(game_id, pull)

                if is_impossible:
                    impossible_game_ids.append(int(game_id))
                    break

    possible_game_ids = [x for x in game_ids if x not in impossible_game_ids]
    print(f"Sum of possible game IDs: {sum(possible_game_ids)}")


if __name__ == "__main__":
    main()
