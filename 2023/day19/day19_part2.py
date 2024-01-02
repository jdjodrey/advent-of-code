import re
from enum import StrEnum
from typing import Optional


class PartResult(StrEnum):
    ACCEPTED = "A"
    REJECTED = "R"


class Part:
    def __init__(self, x: int, m: str, a: str, s: str):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.result = None
        self.workflow_labels = []

    def __repr__(self):
        return f"Part(x={self.x}, m={self.m}, a={self.a}, s={self.s}, result={self.result}, workflows={self.workflow_labels})"


class Rule:
    def __init__(self, category: str, op: str, rating: str, next_step: str):
        self.category = category
        self.op = op
        self.rating = int(rating)
        self.next_step = PartResult(next_step) if next_step in ["A", "R"] else next_step

    def split_part(self, part: Part) -> list[tuple[Part, Optional[str]]]:
        part_range = getattr(part, self.category)

        slice_idx = part_range.index(self.rating)
        if self.op == ">":
            slice_idx += 1

        lower = part_range[:slice_idx]
        upper = part_range[slice_idx:]

        # create new lower part
        lower_part = Part(x=part.x, m=part.m, a=part.a, s=part.s)
        lower_part.workflow_labels = part.workflow_labels.copy()
        setattr(lower_part, self.category, lower)

        # create new upper part
        upper_part = Part(x=part.x, m=part.m, a=part.a, s=part.s)
        upper_part.workflow_labels = part.workflow_labels.copy()
        setattr(upper_part, self.category, upper)

        lower_next_step = self.next_step if self.op == "<" else None
        upper_next_step = self.next_step if self.op == ">" else None

        return [(lower_part, lower_next_step), (upper_part, upper_next_step)]

    def __repr__(self):
        return (
            f"Rule({self.category} {self.op} {self.rating}, next_step={self.next_step})"
        )


class Workflow:
    def __init__(self, label: str, rule_str_list: list[str], default_action: str):
        self.label = label
        self.rules: list[Rule] = self.parse_rules(rule_str_list)
        self.default_action = default_action

    def parse_rules(self, rule_str_list: list[str]) -> list[Rule]:
        rules = []
        for rule_str in rule_str_list.split(","):
            parsed_rule = re.search(r"(\w)([<>])(\d+):(\w+)", rule_str).groups()
            rules.append(Rule(*parsed_rule))

        return rules

    def __repr__(self):
        return f"Workflow(label={self.label}, rules={self.rules}, default_action={self.default_action})"


class System:
    def __init__(self, workflows_str_list: list[str]):
        """
        Example workflow string: px{a<2006:qkq,m>2090:A,rfg}
        """

        self.workflows_by_label: dict[str, Workflow] = self.parse_workflows(
            workflows_str_list
        )

        self.accepted_part_ranges = []
        self.rejected_part_ranges = []

    def parse_workflows(self, workflows_str_list: list[str]) -> list[Workflow]:
        workflows_by_label = {}
        for workflow_str in workflows_str_list:
            label, rule_str_list, default = re.search(
                r"(\w+){(.*),(\w+)}", workflow_str
            ).groups()
            workflows_by_label[label] = Workflow(label, rule_str_list, default)

        return workflows_by_label

    def process_part_in_workflow(
        self, workflow: Workflow, part: Part, levels=0, debug=False
    ):
        part_to_process = part
        part_to_process.workflow_labels.append(workflow.label)

        if (
            len(set([r.next_step for r in workflow.rules] + [workflow.default_action]))
            > 1
        ):
            for rule in workflow.rules:
                if debug:
                    print(100 * "-")
                    print(f"{(levels * 2) * '-'}> {workflow}")
                    print(f"{(levels * 2) * '-'}> {rule}")
                    print(f"{(levels * 2) * '-'}> {part_to_process}")

                split_parts = rule.split_part(part_to_process)

                if debug:
                    print(
                        f"{(levels * 2) * '-'}> SPLIT by {rule.category} {rule.op} {rule.rating}"
                    )

                for split_part, next_step in split_parts:
                    if next_step in [PartResult.ACCEPTED, PartResult.REJECTED]:
                        self.update_part_result(split_part, next_step, levels)
                    elif next_step in self.workflows_by_label.keys():
                        next_workflow = self.workflows_by_label[next_step]
                        self.process_part_in_workflow(
                            next_workflow, split_part, levels=levels + 1
                        )
                    else:
                        part_to_process = split_part
        elif debug:
            print(f"{(levels * 2) * '-'}> All outcomes are the same: {workflow}")

        if workflow.default_action in self.workflows_by_label.keys():
            default_workflow = self.workflows_by_label[workflow.default_action]
            self.process_part_in_workflow(
                default_workflow, part_to_process, levels=levels + 1
            )
        else:
            self.update_part_result(part_to_process, workflow.default_action, levels)

    """
    process ranges of ratings starting with range(1, 4001)
    split ranges on rule processing, e.g. a<2006:qkq would result in two parts:

    Example:
    Workflow a<2006:qkq, m>2090:A, rfg
    0: Part(x=range(1, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001))
        1: Part(x=range(1, 2006), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001))    --> qkq
        2: Part(x=range(2006, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001)) --> m>2090:A,rfg
            2a: Part(x=range(2006, 4001), m=range(2091, 4001), a=range(1, 4001), s=range(1, 4001)) --> A
            2b: Part(x=range(2006, 4001), m=range(1, 2090), a=range(1, 4001), s=range(1, 4001)) --> rfg

    Three possible outcomes after workflow #1:
        - x=range(1, 2006) --> qkq
        - x=range(2006, 4001), m=range(2091, 4001) --> A
        - x=range(2006, 4001), m=range(1, 2090) --> rfg
    """

    def update_part_result(
        self, part: Part, result: PartResult, levels, debug=False
    ) -> None:
        part.result = result
        result_str = "ACCEPTED" if result == PartResult.ACCEPTED else "REJECTED"

        if debug:
            print(100 * "#")
            print(f"{(levels * 2) * '-'}> {result_str} {part}")
            print(100 * "#")

        if result == PartResult.ACCEPTED:
            self.accepted_part_ranges.append(
                {"x": part.x, "m": part.m, "a": part.a, "s": part.s}
            )

        elif result == PartResult.REJECTED:
            self.rejected_part_ranges.append(
                {"x": part.x, "m": part.m, "a": part.a, "s": part.s}
            )
        else:
            raise ValueError(f"Invalid PartResult: {result}")

    def process_parts(self) -> None:
        initial_workflow = self.workflows_by_label["in"]
        initial_part = Part(
            x=range(1, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001)
        )

        self.process_part_in_workflow(initial_workflow, initial_part)


def main():
    workflows = []

    with open("../inputs/day19_input.txt", encoding="utf-8") as f:
        read_data = f.read()

        for line in read_data.splitlines():
            if not len(line.strip()):
                continue

            if not line.startswith("{"):
                workflows.append(line)

    system = System(workflows)

    """
    process ranges of ratings starting with range(1, 4001)
    split ranges on rule processing, e.g. a<2006:qkq would result in two parts:

    Example:
    Workflow a<2006:qkq, m>2090:A, rfg
    0: Part(x=range(1, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001))
        1: Part(x=range(1, 2006), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001))    --> qkq
        2: Part(x=range(2006, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001)) --> m>2090:A,rfg
            2a: Part(x=range(2006, 4001), m=range(2091, 4001), a=range(1, 4001), s=range(1, 4001)) --> A
            2b: Part(x=range(2006, 4001), m=range(1, 2090), a=range(1, 4001), s=range(1, 4001)) --> rfg

    Three possible outcomes after workflow #1:
        - x=range(1, 2006) --> qkq
        - x=range(2006, 4001), m=range(2091, 4001) --> A
        - x=range(2006, 4001), m=range(1, 2090) --> rfg
    """

    system.process_parts()

    num_possible_accepted = []
    for part_range in system.accepted_part_ranges:
        num_possible_accepted.append(
            len(part_range["x"])
            * len(part_range["m"])
            * len(part_range["a"])
            * len(part_range["s"])
        )
    print(sum(num_possible_accepted))


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
