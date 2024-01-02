import re


MAX_BLUES = 14
MAX_GREENS = 13
MAX_REDS = 12

game_id_regex = re.compile("Game (\d+): (.*$)")
game_regex = re.compile("(\d+) (blue|green|red)")

cube_powers = []


def main():
    debug = False
    with open("../inputs/day2_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            game_id = game_id_regex.match(line).group(1)
            pulls = game_id_regex.match(line).group(2)

            game = re.findall(game_regex, pulls)
            # [('3', 'blue'), ('7', 'green'), ('10', 'red'), ('4', 'green'), ('4', 'red'), ('1', 'green'), ('7', 'blue'), ('5', 'red')]
            reds = [int(x[0]) for x in game if x[1] == "red"]
            greens = [int(x[0]) for x in game if x[1] == "green"]
            blues = [int(x[0]) for x in game if x[1] == "blue"]

            max_red = max(reds)
            max_green = max(greens)
            max_blue = max(blues)
            if debug:
                print(
                    f"Game {game_id} - {max_red} {max_green} {max_blue} - {max_red * max_green * max_blue}"
                )
            cube_powers.append(max_red * max_green * max_blue)

    print(sum(cube_powers))


if __name__ == "__main__":
    main()
