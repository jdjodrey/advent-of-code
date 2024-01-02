import re


"""

Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules;
they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input.
Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.

"""


class Module:
    def __init__(self, label: str, outputs: list[str]):
        self.label = label
        self.outputs = outputs

    def __repr__(self) -> str:
        return f"Module(label={self.label}, outputs={self.outputs})"


class FlipFlop(Module):
    """
    Flip-flop modules (prefix %) are either on or off; they are initially off.
    If a flip-flop module receives a high pulse, it is ignored and nothing happens.
    However, if a flip-flop module receives a low pulse, it flips between on and off.
    If it was off, it turns on and sends a high pulse.
    If it was on, it turns off and sends a low pulse.
    """

    def __init__(self, label: str, outputs: list[str]):
        super().__init__(label, outputs)
        self.state = False

    def process_pulse(self, pulse: bool, *_):
        if pulse:
            return

        self.state = not self.state
        return self.state

    def __repr__(self):
        return (
            f"FlipFlop(label={self.label}, outputs={self.outputs}, state={self.state})"
        )


class Conjunction(Module):
    """
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules;
    they initially default to remembering a low pulse for each input.
    When a pulse is received, the conjunction module first updates its memory for that input.
    Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    """

    def __init__(self, label: str, outputs: list[str]):
        super().__init__(label, outputs)
        self.inputs = {}
        self.sorted_input_labels = []

    def process_pulse(self, pulse: bool, input_label: str):
        self.inputs[input_label] = pulse
        return not all(self.inputs.values())

    def __repr__(self):
        # return f"Conjunction(label={self.label}, outputs={self.outputs}, inputs={self.inputs}, sorted_input_labels={self.sorted_input_labels})"
        return f"Conjunction(label={self.label}, inputs={''.join(['1' if self.inputs[label] else '0' for label in self.sorted_input_labels])})"


class Broadcaster(Module):
    def process_pulse(self, pulse: bool, *_):
        return pulse

    def __repr__(self):
        return f"Broadcaster(label={self.label}, outputs={self.outputs})"


class Controller:
    def __init__(self, modules: list[Module]):
        self.modules = modules
        self.modules_by_label = {module.label: module for module in modules}
        self.num_pulses_sent = {True: 0, False: 0}

        self.cs_module_cur_state = [False, False, False, False]
        self.cs_module_state_history = [[False, False, False, False]]

        self.termination_module = Module("output", [])

        self.init_conjunction_inputs()

    def init_conjunction_inputs(self):
        for module in self.modules:
            output_modules = [
                self.modules_by_label.get(output) for output in module.outputs
            ]
            for output_module in output_modules:
                if isinstance(output_module, Conjunction):
                    output_module.inputs[module.label] = False

        for module in self.modules:
            if isinstance(module, Conjunction):
                module.sorted_input_labels = sorted(module.inputs.keys())

    def get_output_modules(self, module: Module):
        return [
            self.modules_by_label[output]
            if output in self.modules_by_label
            else self.termination_module
            for output in module.outputs
        ]

    def push_button(self, num_presses=0, debug=False):
        pulses_to_send = [(self.modules_by_label["broadcaster"], False)]
        self.num_pulses_sent[False] += 1

        if debug:
            print("button -> low -> broadcaster")

        while len(pulses_to_send):
            module, pulse = pulses_to_send.pop(0)
            for output_module in self.get_output_modules(module):
                self.num_pulses_sent[pulse] += 1

                if output_module.label == "rx" and not pulse:
                    return True

                if debug:
                    print(
                        f"{module.label} -> {'high' if pulse else 'low'} -> {output_module.label}"
                    )

                if output_module == self.termination_module:
                    continue

                new_pulse = output_module.process_pulse(pulse, module.label)

                if output_module.label == "cs":
                    cur_state = [
                        output_module.inputs[label]
                        for label in output_module.sorted_input_labels
                    ]
                    if cur_state != self.cs_module_cur_state:
                        self.print_conjunction_debug(module, cur_state, num_presses)
                        # if cur_state.count(True) == 2:
                        #     print(
                        #         f"#{num_presses}| input={module.label} new={cur_state}"
                        #     )
                        #     return True

                        self.cs_module_cur_state = cur_state
                        self.cs_module_state_history.append(cur_state)

                if new_pulse is not None:
                    pulses_to_send.append((output_module, new_pulse))

        return False

    def print_conjunction_debug(self, module, new_cs_state, num_presses):
        self.print_system_state(num_presses=num_presses, conjunctions_only=True)

    def print_system_state(self, num_presses=0, conjunctions_only=False):
        print(f"{20 * '-'}{num_presses}{20 * '-'}")
        for module in self.modules:
            if conjunctions_only and not isinstance(module, Conjunction):
                continue
            print(module)
        print(50 * "-")


def main():
    modules = []

    with open("../inputs/day20_input.txt", encoding="utf-8") as f:
        read_data = f.read()

        for line in read_data.splitlines():
            inputs, outputs = re.search(r"(.*) -> (.*)", line).groups()
            outputs = [output.strip() for output in outputs.split(", ")]

            if inputs.startswith("%"):
                module = FlipFlop(inputs[1:], outputs)
            elif inputs.startswith("&"):
                module = Conjunction(inputs[1:], outputs)
            else:
                module = Broadcaster(inputs, outputs)

            modules.append(module)

    controller = Controller(modules)

    button_presses = 0
    pulsed_rx = False
    while not pulsed_rx:
        button_presses += 1
        pulsed_rx = controller.push_button(num_presses=button_presses)

        if button_presses % 100000 == 0:
            print(f"Button presses sent: {button_presses}")

        if button_presses > 5000000:
            break

    print(f"Button presses sent: {button_presses}")


"""
print all conjunction module states and their inputs

259344259180561 is too high (4013^4)

228745085711041 is wrong (3889^4)
214951987660081 is wrong (3829^4)
214846439684881 is wrong (14657641^2)

201792281140321 is too low (3769^4)

Two Trues at 14,657,641

[hn, kh, lz, tg]

#14657641| input=kh old=[False, False, False, False] new=[False, True, False, False]
input_module=hn input state=[True]
input_module=kh input state=[False]
input_module=lz input state=[True]
input_module=tg input state=[False]

#14657641| input=tg old=[False, True, False, False] new=[False, True, False, True]
input_module=hn input state=[True]
input_module=kh input state=[False]
input_module=lz input state=[True]
input_module=tg input state=[False]

#14657641| input=kh old=[False, True, False, True] new=[False, False, False, True]
input_module=hn input state=[True]
input_module=kh input state=[True]
input_module=lz input state=[True]
input_module=tg input state=[True]

#14657641| input=tg old=[False, False, False, True] new=[False, False, False, False]
input_module=hn input state=[True]
input_module=kh input state=[True]
input_module=lz input state=[True]
input_module=tg input state=[True]

#14659489| input=hn old=[False, False, False, False] new=[True, False, False, False]
input_module=hn input state=[False]
input_module=kh input state=[True]
input_module=lz input state=[True]
input_module=tg input state=[True]

#14659489| input=hn old=[True, False, False, False] new=[False, False, False, False]
input_module=hn input state=[True]
input_module=kh input state=[True]
input_module=lz input state=[True]
input_module=tg input state=[True]

#14661331| input=lz old=[False, False, False, False] new=[False, False, True, False]
input_module=hn input state=[True]
input_module=kh input state=[True]
input_module=lz input state=[False]
input_module=tg input state=[True]
#14661331| input=lz old=[False, False, True, False] new=[False, False, False, False]
input_module=hn input state=[True]
input_module=kh input state=[True]
input_module=lz input state=[True]
input_module=tg input state=[True]


Conjunction(label=kh, inputs=1)
Conjunction(label=zv, inputs=011000111)
Conjunction(label=sk, inputs=0110001)
Conjunction(label=lz, inputs=1)
Conjunction(label=tg, inputs=1)
Conjunction(label=hn, inputs=1)
Conjunction(label=pl, inputs=00001101)
Conjunction(label=cs, inputs=0000)
Conjunction(label=sd, inputs=01110000)
--------------------------------------------------
Conjunction(label=kh, inputs=1)
Conjunction(label=zv, inputs=000000100)
Conjunction(label=sk, inputs=1100101)
Conjunction(label=lz, inputs=1)
Conjunction(label=tg, inputs=1)
Conjunction(label=hn, inputs=1)
Conjunction(label=pl, inputs=10001011)
Conjunction(label=cs, inputs=0000)
Conjunction(label=sd, inputs=11110101)
--------------------------------------------------
Button presses sent: 1000000
--------------------------------------------------
Conjunction(label=kh, inputs=1)
Conjunction(label=zv, inputs=111101000)
Conjunction(label=sk, inputs=0100001)
Conjunction(label=lz, inputs=1)
Conjunction(label=tg, inputs=1)
Conjunction(label=hn, inputs=1)
Conjunction(label=pl, inputs=01110111)
Conjunction(label=cs, inputs=0000)
Conjunction(label=sd, inputs=10101100)
"""

if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
