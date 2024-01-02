def main():
    histories = []
    with open("../inputs/day9_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for line in read_data.splitlines():
            histories.append([int(x) for x in line.split()])

    line_histories = []
    for line in histories:
        line_history = [line]
        next_seq = [line[x] - line[x - 1] for x in range(1, len(line))]
        line_history.append(next_seq)

        # while next seq isn't all zeros
        while next_seq.count(0) != len(next_seq):
            next_seq = [next_seq[x] - next_seq[x - 1] for x in range(1, len(next_seq))]
            line_history.append(next_seq)

        line_history[-1].append(0)

        line_histories.append(line_history)

    for line_history in line_histories:
        # iterate backwards through each sequence history, skipping the first one
        for idx in range(len(line_history) - 1, 1, -1):
            seq = line_history[idx - 2]
            prev_seq = line_history[idx - 1]
            last_num = seq[-1]
            last_prev_num = prev_seq[-1]
            seq.append(last_num + last_prev_num)

    final_nums = [x[0][-1] for x in line_histories]
    print(sum(final_nums))


if __name__ == "__main__":
    main()
