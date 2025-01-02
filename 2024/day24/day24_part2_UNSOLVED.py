import re
import time
from enum import StrEnum


class GateOp(StrEnum):
    AND = "&"
    OR = "|"
    XOR = "^"


class Wire:
    def __init__(self, label: str, value: int | None = None):
        self.label = label
        self.value = value

    def __repr__(self):
        return f"{self.label}={self.value}"

class Gate:
    def __init__(self, inputs: list[Wire], output: Wire, op: GateOp):
        self.inputs = inputs
        self.output = output
        self.op = op


def get_input() -> tuple[dict[str, Wire], list[Gate]]:
    gates_re = re.compile(r"((?:\w|\d){3}) (AND|OR|XOR) ((?:\w|\d){3}) -> ((?:\w|\d){3})")
    parse_gates = False

    wires_by_label: dict[str, Wire] = {}
    gates: list[Gate] = []
    with open("../inputs/day24_input.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            if not line:
                parse_gates = True
                continue

            if not parse_gates:
                label, value = line.split(": ")
                wires_by_label[label] = Wire(label, value)
            else:
                input_label1, op, input_label2, output_label = re.findall(gates_re, line)[0]

                input_wire1 = wires_by_label.get(input_label1, Wire(input_label1))
                wires_by_label[input_label1] = input_wire1

                input_wire2 = wires_by_label.get(input_label2, Wire(input_label2))
                wires_by_label[input_label2] = input_wire2

                output_wire = wires_by_label.get(output_label, Wire(output_label))
                wires_by_label[output_label] = output_wire

                gate = Gate([input_wire1, input_wire2], output_wire, GateOp[op])
                gates.append(gate)

    return wires_by_label, gates


def reset(wires_by_label, idx) -> tuple[dict, dict]:
    x_wires_by_label: dict[str, Wire] = {}
    for label, w in wires_by_label.items():
        if label.startswith("x"):
            w.value = 0
            x_wires_by_label[label] = w

    y_wires_by_label: dict[str, Wire] = {}
    for label, w in wires_by_label.items():
        if label.startswith("y"):
            w.value = 0
            y_wires_by_label[label] = w

    # y_wires_by_label["y00"].value = 1
    #
    x_label = f"x{'0' if idx < 10 else ''}{idx}"
    x_wires_by_label[x_label].value = 1

    # x_wires_by_label["x00"].value = 1

    # y_label = f"y{'0' if idx < 10 else ''}{idx}"
    # y_wires_by_label[y_label].value = 1

    return x_wires_by_label, y_wires_by_label


def main():

    problem_wires = []
    for idx in range(45):
        wires_by_label, gates = get_input()

        x_wires_by_label, y_wires_by_label = reset(wires_by_label, idx)

        x_wires = list(x_wires_by_label.values())
        x_wires.sort(key=lambda w: w.label, reverse=True)
        x_value = "".join([str(x.value) for x in x_wires])
        print(x_value, int(x_value, 2))

        y_wires = list(y_wires_by_label.values())
        y_wires.sort(key=lambda w: w.label, reverse=True)
        y_value = "".join([str(y.value) for y in y_wires])
        print(y_value, int(y_value, 2))

        while any(w.value is None for w in wires_by_label.values()):
            for g in gates:
                input1 = g.inputs[0].value
                input2 = g.inputs[1].value
                if input1 is not None and input2 is not None:
                    g.output.value = eval(f"{input1} {g.op} {input2}")

        z_wires: list[Wire] = []
        for label, w in wires_by_label.items():
            if label.startswith("z"):
                z_wires.append(w)

        z_wires.sort(key=lambda w: w.label, reverse=True)

        binary_value = "".join([str(w.value) for w in z_wires])
        print(f"Total: {int(binary_value, 2)}")
        if int(x_value, 2) + int(y_value, 2) != int(binary_value, 2):
            x_label = f"x{'0' if idx < 10 else ''}{idx}"
            x_wire = x_wires_by_label[x_label]
            print(f"Issue with {x_label}")

            for g in gates:
                if x_wire in g.inputs:
                    print(f"Problem wire: {g.output.label}")
                    problem_wires.append(g.output.label)

    print(",".join([w for w in sorted(problem_wires)]))

    # bdr,dkk,fwr,hpw,nbc,nrj,svm,z23 isn't correct

    # dkk,fnr,fwr,hpw,nbc,svm,z23,z39 isn't correct

    # 70368744000000
    # 70368735723518

    # bdr,dkk,fwr,hpw,nbc,nrj,svm,z23
    # bdr,dkk,fwr,hpw,nbc,nrj,svm,z23
    # dkk,dwt,fwr,gsb,hpw,mdg,nbc,phv,smn,svm,wfh,z23
    # dkk,fwr,hpw,nbc,svm,z23

    # bdr,dkk,fwr,hpw,nrj,z23
    # bdr,dkk,fwr,hpw,nrj,z23
    # dkk,dwt,fwr,gsb,hpw,mdg,phv,smn,wfh,z23
    # dkk,fwr,hpw,z23

    # bdr,fwr,hpw,nrj,wfh,z23
    # bdr,fwr,hpw,nrj,wfh,z23
    # dwt,gsb,hpw,phv,smn,z23
    #

    # dkk and wfh MAYBE?
    # dwt and z23
    # gsb and phv

    # svm and nbc CONFIRMED
    # dkk and wfh I THINK
    # dwt and z23 I THINK

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")