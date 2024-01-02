import re
import time
from itertools import groupby


def main():
    records = []
    with open("../inputs/day12_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            springs, groups = line.split()
            records.append(
                {
                    "springs": springs,
                    "groups": [int(grp) for grp in groups.split(",")],
                    "num_configurations": 0,
                }
            )
            records.append(
                {
                    "springs": f"{springs}?",
                    "groups": [int(grp) for grp in groups.split(",")],
                    "num_configurations": 0,
                }
            )
            # records.append(
            #     {
            #         "springs": "?".join([springs] * 2),
            #         "groups": [int(grp) for grp in ",".join([groups] * 2).split(",")],
            #         "num_configurations": 0,
            #     }
            # )

    def optimization_pass_1a(spring_groups, groups):
        """
        if first element has less characters than first group, drop it
        if last element has less characters than last group, drop it
        Example: ?.?#??#??..# 3,1,1 --> ?#??#??..# 3,1,1
        """

        while len(spring_groups) and len(spring_groups[0]) < groups[0]:
            spring_groups.pop(0)

        while len(spring_groups) and len(spring_groups[-1]) < groups[-1]:
            spring_groups.pop(-1)

        return spring_groups, groups

    def optimization_pass_1b(spring_groups, groups):
        """
        if first element has same number of # as first group, drop it and the group
        if last element has same number of # as last group, drop it and the group
        Example: .#.?#?.???. 1,3,2 -> ?#?.???. --> 3,2
        """

        while (
            len(spring_groups)
            and len(groups)
            and set(spring_groups[0]) == {"#"}
            and spring_groups[0].count("#") == groups[0]
        ):
            spring_groups.pop(0)
            groups.pop(0)

        while (
            len(spring_groups)
            and len(groups)
            and set(spring_groups[-1]) == {"#"}
            and spring_groups[-1].count("#") == groups[-1]
        ):
            spring_groups.pop(-1)
            groups.pop(-1)

        return spring_groups, groups

    def optimization_pass_1c(spring_groups, groups):
        """
        if first element has same number of characters as first group AND contains a #, drop it and the group
        if last element has same number of characters as last group AND contains a #, drop it and the group
        Example: ??#?.????? 4,2 --> ????? --> 2
                 ???????..?##??? 4,6 --> ??????? 4
        """

        while (
            len(spring_groups)
            and len(groups)
            and len(spring_groups[0]) == groups[0]
            and spring_groups[0].count("#") > 0
        ):
            spring_groups.pop(0)
            groups.pop(0)

            if not len(spring_groups) or not len(groups):
                break

        while (
            len(spring_groups)
            and len(groups)
            and len(spring_groups[-1]) == groups[-1]
            and spring_groups[-1].count("#") > 0
        ):
            spring_groups.pop(-1)
            groups.pop(-1)

        return spring_groups, groups

    def optimization_pass_1d(spring_groups, groups):
        debug = bool(groups == [3, 2, 1, 3, 2, 1]) and False
        """
        1c: ['?###??????????###????????'] [3, 2, 1, 3, 2, 1]
        1d: ['.....?????????...??????'] [2, 1, 2, 1]
        """
        clusters = [
            (label, sum(1 for _ in group))
            for label, group in groupby(".".join(spring_groups))
        ]

        # [('.', 1), ('?', 1), ('#', 3), ('?', 10), ('#', 3), ('?', 8), ('.', 1)]
        # if the highest group is equal to the longest contiguous # group
        # you can drop that group num and the # group (and decrement left/right ? groups by 1)

        biggest_group = max(groups)
        for idx, cluster in enumerate(clusters):
            if cluster[0] == "#" and biggest_group == cluster[1]:
                prev_cluster = clusters[idx - 1] if idx > 0 else None
                next_cluster = clusters[idx + 1] if idx < len(clusters) - 1 else None

                if debug:
                    breakpoint()
                if prev_cluster and prev_cluster[0] == "?":
                    clusters[idx - 1] = (prev_cluster[0], max(prev_cluster[1] - 1, 0))

                if next_cluster and next_cluster[0] == "?":
                    clusters[idx + 1] = (next_cluster[0], max(next_cluster[1] - 1, 0))

                groups.pop(groups.index(biggest_group))
                clusters[idx] = (".", 1)

                if len(groups):
                    biggest_group = max(groups)
                else:
                    break

        # reassemble
        ret_springs = "".join([cluster[0] * cluster[1] for cluster in clusters])
        if debug:
            breakpoint()
        return [s for s in ret_springs.split(".") if len(s) > 0], groups

    def get_possibilities_for_single_group(num_unknowns, group_size):
        """
        if there's only one group and the record is all ?, then the number of configurations is equal to
        the number of ways can you slice a record of length N into groups of size M --> N - M + 1
        Example: ????? 2 --> 5 - 2 + 1 = 4 configurations
                 ?????????? 1 --> 10 - 1 + 1 = 10 configurations
        """
        return num_unknowns - group_size + 1

    def calc_possible_configs(rec):
        springs = rec["springs"]
        num_unknowns = springs.count("?")
        possibilities = 2**num_unknowns

        replace_idx = [m.start() for m in re.finditer(re.escape("?"), rec["springs"])]
        springs_list = list(springs)
        total_springs = sum(rec["groups"])
        num_springs = rec["springs"].count("#")
        for num in range(possibilities):
            # if there's not enough #'s and 1's to equal the sum of groups, skip
            num_ones = num.bit_count()
            if num_ones + num_springs != total_springs:
                continue

            bin_str = bin(num)[2:].zfill(num_unknowns)

            for idx, j in enumerate(replace_idx):
                springs_list[j] = spring_mapping[bin_str[idx]]

            springs = "".join(springs_list)

            spring_groups = [s for s in springs.split(".") if s.count("#") > 0]
            if len(spring_groups) != len(rec["groups"]):
                continue

            if all(
                [
                    len(spring_group) == grp
                    for spring_group, grp in zip(spring_groups, rec["groups"])
                ]
            ):
                rec["num_configurations"] += 1

        return rec

    """
    APPLY PRE-OPTIMIZATIONS

    Example of multiple optimizations:
    Start:      ???????..?##???.? 4,6 
    Apply 1A:   ???????..?##??? 4,6
    Apply 1C:   ??????? 4
    Apply 2A:    N - M + 1 --> 7 - 4 + 1 = 4 configurations
    """
    for rec in records:
        # print(f"Original: {rec['springs']} {rec['groups']}")
        spring_groups = [s for s in rec["springs"].split(".") if len(s) > 0]
        groups = rec["groups"]

        # print(f"Original: {rec['springs']} {groups}")
        spring_groups, groups = optimization_pass_1a(spring_groups, groups)
        # print(f"1a: {spring_groups} {groups}")
        spring_groups, groups = optimization_pass_1b(spring_groups, groups)
        # print(f"1b: {spring_groups} {groups}")
        spring_groups, groups = optimization_pass_1c(spring_groups, groups)
        # print(f"1c: {spring_groups} {groups}")
        # spring_groups, groups = optimization_pass_1d(spring_groups, groups)
        # print(f"1d: {spring_groups} {groups}")

        if len(groups) == 1 and spring_groups[0].count("?") == len(spring_groups[0]):
            rec["num_configurations"] = get_possibilities_for_single_group(
                spring_groups[0].count("?"), groups[0]
            )
        else:
            rec[
                "springs"
            ] = f"{'.' if rec['springs'].startswith('.') else ''}{'.'.join(spring_groups)}{'.' if rec['springs'].endswith('.') else ''}"
            rec["groups"] = groups

    # print(f"New: {rec['springs']} {rec['groups']} {rec['num_configurations']}")

    spring_mapping = {"1": "#", "0": "."}
    possibilities = []
    for rec_idx, rec in enumerate(records):
        if rec["num_configurations"] > 0:
            # print(
            #     f"!{rec['springs']} {rec['groups']} -> {rec['num_configurations']} configs"
            # )
            continue

        springs = rec["springs"]
        # possibilities.append(
        #     {"springs": springs, "groups": rec["groups"], "num": springs.count("?")}
        # )

        # continue

        # print(f"Processing {springs} {rec['groups']}")

        """
        additional optimization idea

        ..???#??????#?????? 3,6
        
        if there's only one spring group (i.e. it's all ?'s and #'s)
        and the first # appears within the first group size ([0:group_size+1])
        slice off [0:(index_of_first_# + group_size)]
        ..???#??????#?????? 3,6
        becomes
        ???#?? 3
        ????#?????? 6
        find possibilities for each and multiply them together
        """

        """
        need to figure out how to make it work with more than 2 groups
        ??#?????????#?##?????#?????????#?##??? 4,4,2,4,4,4,2,4
        ------
        ??#??? 4
        ??????#?##?????#?????????#?##??? 4,2,4,4,4,2,4

        ?###??????????###???????? 3,2,1,3,2,1
        ?###? 3
        ???????? 2,1
        ?###? 3
        ??????? 2,1

        """
        """
        another idea
        iterate over and see where you can fit the first group
        ?###??????????###???????? 3,2,1,3,2,1

        ?###? 3
        ???????? 2
        ?###???????? 1,3,2,1
        
        search for 2 but leave space for [1,3,2,1] + len + 1
        
        """
        if set(springs.strip(".")) == {"#", "?"}:
            if "#" in springs[: rec["groups"][0] + 1]:
                groups = [n for n in rec["groups"]]
                springs1 = springs[: springs.index("#") + rec["groups"][0]]
                springs2 = springs[springs.index("#") + rec["groups"][0] :]
                # breakpoint()
                r1 = calc_possible_configs(
                    {
                        "springs": springs1,
                        "groups": [groups.pop(0)],
                        "num_configurations": 0,
                    }
                )
                if springs1.endswith("#"):
                    springs2 = springs2[1:]
                r2 = calc_possible_configs(
                    {
                        "springs": springs2,
                        "groups": groups,
                        "num_configurations": 0,
                    }
                )
                # breakpoint()

                rec["num_configurations"] = (
                    r1["num_configurations"] * r2["num_configurations"]
                )
                # print(
                #     f"{springs} combined {r1['num_configurations']} * {r2['num_configurations']} = {rec['num_configurations']}"
                # )
                # subtract 1 because # can't be adjancent to another # (i.e. last # of group1 and first # of group2)
                # rec["num_configurations"] -= 1
                # breakpoint()
                continue

        """
        more optimization ideas
        if there's a leading . (e.g. ..???#??????#?????? 3,6) and one spring group then we can optimize processing the next record
        ..???#??????#?????? will become ..???#??????#???????..???#??????#?????? 3,6,3,6
        which we can reduce to ..???#??????#??????? 3,6 + num configs from the previous record
        """
        lookahead = springs.startswith(".") and set(springs.strip(".")) == {"#", "?"}

        rec = calc_possible_configs(rec)

        if lookahead and springs in records[rec_idx + 1]["springs"]:
            next_rec = calc_possible_configs(
                {
                    "springs": rec["springs"] + "?",
                    "groups": rec["groups"],
                    "num_configurations": 0,
                }
            )

            records[rec_idx + 1]["num_configurations"] = (
                next_rec["num_configurations"] + rec["num_configurations"]
            )

        # print(
        #     f"{rec['springs']} {rec['groups']} -> {rec['num_configurations']} configs"
        # )

    # breakpoint()
    # sort possibilities by number of unknowns
    # possibilities.sort(key=lambda x: x["num"])

    # for i in range(1, 20):
    #     print(possibilities[-i])

    # print(len([p for p in possibilities if p["num"] > 30]))
    # return

    for idx, rec in enumerate(records):
        print(
            f"{rec['springs']} {rec['groups']} -> {rec['num_configurations']} configs"
        )
        if (idx + 1) % 2 == 0:
            print(25 * "-")

    multiplied_records = []
    # print(25 * "-")
    for idx in range(1, len(records), 2):
        rec = records[idx]
        prev_rec = records[idx - 1]

        # multiplier = rec["num_configurations"] // prev_rec["num_configurations"]
        multiplier = (
            rec["num_configurations"] * prev_rec["num_configurations"]
        ) // prev_rec["num_configurations"]
        print(
            f"{rec['springs']} {prev_rec['num_configurations']} * {(multiplier**4)} = {prev_rec['num_configurations'] * (multiplier**4)}"
        )
        rec["num_configurations"] = prev_rec["num_configurations"] * (multiplier**4)
        multiplied_records.append(rec)
        # print(25 * "-")

    # print sum of all configurations
    print(sum([rec["num_configurations"] for rec in multiplied_records]))


def test():
    """
    ?????????????#???.?? 4, 8, 1

    """
    # ??????????#??? | ??????????#??????????????
    # springs = "??????????#???????????????????#????????"
    # nums = [int(g) for g in "7,4,2,7,4,2".split(",")]

    # first_num = nums[0]
    # req_room = sum(nums[1:]) + len(nums) - 1

    # front_springs, back_springs = (
    #     springs[0 : len(nums) - req_room - first_num],
    #     springs[: req_room + 1],
    # )

    # print(f"first_num: {first_num} req_room: {req_room}")
    # print(f"{front_springs} | {back_springs}")
    # print(springs)

    """
    split by . and # and calculate possibilities for each group
    put all the combinations together
    """
    import itertools

    # tmp = list(itertools.product([0, 1], repeat=3))

    springs = "?????????#???????"
    nums = [7, 4, 2, 7, 4, 2]
    trans_table = springs.maketrans("#.", "10")
    springs = springs.translate(trans_table)
    grps = re.split("[1]", springs)
    print(grps)

    possibilities = []
    for idx, g in enumerate(grps):
        if idx < len(grps):
            grp_pos = list(itertools.product([0, 1], repeat=len(g)))
            grp_pos = [x for x in grp_pos if x[-1] == 1]
        possibilities.append(grp_pos)

    total_possibilities = list(itertools.product(*possibilities))
    print(len(total_possibilities))
    print([len(possibilities[i]) for i in range(len(possibilities))])

    """


    BAD  ???.###               [1, 1, 3] -> 1 * (3*4) = 81 (should be 1) WORKS WITH ? SUFFIX
    GOOD .??..??...?##.        [1, 1, 3] -> 4 * (8^4) = 16384
    GOOD ?#?#?#?#?#?#?#?       [1, 3, 1, 6] -> 1 * 1 = 1
    GOOD ????.#...#...         [4, 1, 1] -> 1 * (2^4) = 16
    GOOD ????.######..#####.   [1, 6, 5] -> 4 * (5^4)) = 2500
    BAD  ?###????????          [3, 2, 1] -> 10 * (10^4) = 100000 (should be 10 * (15^4) 506250) WORKS WITH ? SUFFIX
    GOOD .?##???.#?            [3, 2] -> 2 * (2^4) = 32
    GOOD ?.?#??#??..#          [3, 1, 1] -> 1 * 1 = 1
    GOOD ?.?????.??????        [1, 3, 1, 3] -> 16 * 707281 = 11316496
    BAD ??#???????????.??#.?.  [5, 1, 1, 1, 1, 1] -> 54 * (120^4) = 11197440000 (should be 54 * (155^4) = 31168833750)) (num_? - 1 + [sum of groups] = 25) (54 - grp sum)
    BAD ?#??#?#??#?#?.??#??    [11, 4] -> 2 * (2^4) = 32 (should be 2 * (3^4) = 162) WORKS WITH ? SUFFIX
    BAD ??#?????????#?##??     [4, 4, 2, 4] -> 3 * (7^4) = 7203 (should be 3 * 3^4 = 243) (14 ?, sum grps = 14)

    
    ?#???????????.??#.?.? 54 * (131^4)) = 15902995734
    ?#??#?#??#?#?.??#??? 2 * 81 = 162

    ???.###? 1 * 1 = 1
    .??.?? 4 * 256 = 1024
    ?#?#?#?#?#?#?#?? 1 * 1 = 1
    ????.#.#.? 1 * 1 = 1
    ????.######..#####.? 4 * 256 = 1024
    ?###???????? 10 * 50625 = 506250
    ?.?????.??????? 16 * 707281 = 11316496

    ???.### 1,1,3                  
    .??..??...?##. 1,1,3    
    ?#?#?#?#?#?#?#? 1,3,1,6
    ????.#...#... 4,1,1
    ????.######..#####. 1,6,5
    ?###???????? 3,2,1
    ?.?????.?????? 1,3,1,3
    ?.?#??#??..# 3,1,1

    """


if __name__ == "__main__":
    start = time.time()
    main()

    end = time.time()
    print(f"Time1: {end - start}")
