import re
from enum import StrEnum
from typing import Optional, Union


class PartResult(StrEnum):
    ACCEPTED = "A"
    REJECTED = "R"


class Part:
    def __init__(self, x: str, m: str, a: str, s: str):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.result = None
        self.workflow_labels = []
        self.sum = sum([int(x) for x in [self.x, self.m, self.a, self.s]])

    def __repr__(self):
        return f"Part(x={self.x}, m={self.m}, a={self.a}, s={self.s}, result={self.result}, workflows={self.workflow_labels})"


class Rule:
    def __init__(self, category: str, op: str, rating: str, next_step: str):
        self.category = category
        self.op = op
        self.rating = int(rating)
        self.next_step = PartResult(next_step) if next_step in ["A", "R"] else next_step

    def does_part_match(self, part: Part) -> bool:
        part_value = int(getattr(part, self.category))

        if self.op == "<":
            return part_value < self.rating
        elif self.op == ">":
            return part_value > self.rating
        else:
            raise ValueError(f"Invalid operator: {self.op}")

    def __repr__(self):
        return f"Rule(category={self.category}, op={self.op}, rating={self.rating}, next_step={self.next_step})"


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

    def process_part(self, part: Part) -> str:
        part.workflow_labels.append(self.label)
        for rule in self.rules:
            if rule.does_part_match(part):
                return rule.next_step

        return self.default_action

    def __repr__(self):
        return f"Workflow(label={self.label}, rules={self.rules}, default_action={self.default_action})"


class System:
    def __init__(self, workflows_str_list: list[str], parts_str_list: list[str]):
        """
        Example workflow string: px{a<2006:qkq,m>2090:A,rfg}
        Example part string: {x=787,m=2655,a=1222,s=2876}
        """

        self.workflows_by_label: dict[str, Workflow] = self.parse_workflows(
            workflows_str_list
        )
        self.parts: list[Part] = self.parse_parts(parts_str_list)

        self.accepted_parts = []
        self.rejected_parts = []

    def parse_parts(self, parts_str_list: list[str]) -> list[Part]:
        parts = []
        for part_str in parts_str_list:
            parsed_part = re.search(
                r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", part_str
            ).groups()
            parts.append(Part(*parsed_part))

        return parts

    def parse_workflows(self, workflows_str_list: list[str]) -> list[Workflow]:
        workflows_by_label = {}
        for workflow_str in workflows_str_list:
            label, rule_str_list, default = re.search(
                r"(\w+){(.*),(\w+)}", workflow_str
            ).groups()
            workflows_by_label[label] = Workflow(label, rule_str_list, default)

        return workflows_by_label

    def process_parts(self, limit: Optional[int] = None) -> None:
        initial_workflow = self.workflows_by_label["in"]
        for idx, part in enumerate(self.parts):
            if limit and idx == limit:
                break

            next_step = initial_workflow.process_part(part)
            while next_step not in [PartResult.ACCEPTED, PartResult.REJECTED]:
                next_step = self.workflows_by_label[next_step].process_part(part)

            self.update_part_result(part, next_step)

    def update_part_result(self, part: Part, result: str) -> None:
        part.result = result

        if result == PartResult.ACCEPTED:
            self.accepted_parts.append(part)
        elif result == PartResult.REJECTED:
            self.rejected_parts.append(part)

    def display(self, show_workflows: bool = True, show_parts: bool = True) -> None:
        if show_workflows:
            for k, v in self.workflows_by_label.items():
                print(k, v)
                for i, rule in enumerate(v.rules):
                    print(f"  #{i + 1}: {rule}")

        if show_parts:
            for part in self.parts:
                print(part)


def main():
    workflows = []
    parts = []

    with open("../inputs/day19_input.txt", encoding="utf-8") as f:
        read_data = f.read()

        for line in read_data.splitlines():
            if not len(line.strip()):
                continue

            if line.startswith("{"):
                parts.append(line)
            else:
                workflows.append(line)

    system = System(workflows, parts)

    system.process_parts()

    print(f"Sum of accepted parts: {sum([p.sum for p in system.accepted_parts])}")


if __name__ == "__main__":
    import time

    start = time.time()
    main()
    print(f"Time: {time.time() - start}")
