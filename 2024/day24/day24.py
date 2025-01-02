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


def main():
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
    print(int(binary_value, 2))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")