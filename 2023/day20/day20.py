import re


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

    def process_pulse(self, pulse: bool, input_label: str):
        self.inputs[input_label] = pulse
        return not all(self.inputs.values())

    def __repr__(self):
        return f"Conjunction(label={self.label}, outputs={self.outputs}, inputs={self.inputs})"


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

    def get_output_modules(self, module: Module):
        return [
            self.modules_by_label[output]
            if output in self.modules_by_label
            else self.termination_module
            for output in module.outputs
        ]

    def push_button(self, debug=False):
        pulses_to_send = [(self.modules_by_label["broadcaster"], False)]
        self.num_pulses_sent[False] += 1

        if debug:
            print("button -> low -> broadcaster")

        while len(pulses_to_send):
            module, pulse = pulses_to_send.pop(0)
            for output_module in self.get_output_modules(module):
                self.num_pulses_sent[pulse] += 1

                if debug:
                    print(
                        f"{module.label} -> {'high' if pulse else 'low'} -> {output_module.label}"
                    )

                if output_module == self.termination_module:
                    continue

                new_pulse = output_module.process_pulse(pulse, module.label)

                if new_pulse is not None:
                    pulses_to_send.append((output_module, new_pulse))

    def print_system_state(self):
        for module in self.modules:
            print(module)

        print(f"Number of pulses sent: {self.num_pulses_sent}")


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

    for _ in range(1000):
        controller.push_button()

    pulses_sent = controller.num_pulses_sent
    print(
        f"Pulses sent: {pulses_sent[False]} (low) * {pulses_sent[True]} (high) = {pulses_sent[False] * pulses_sent[True]}"
    )


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
