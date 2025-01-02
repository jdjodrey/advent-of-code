import math
import re
import time


class Program:
    def __init__(self, reg_a: int, reg_b: int, reg_c: int, program: str):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.program: list[int] = [int(x) for x in program.split(",")]
        self.pointer: int = 0
        self.output = []

        self.combo_operands = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3,
            4: self._get_reg_a,
            5: self._get_reg_b,
            6: self._get_reg_c
        }

        self.instructions = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

    def _get_reg_a(self) -> int:
        return self.reg_a

    def _get_reg_b(self) -> int:
        return self.reg_b

    def _get_reg_c(self) -> int:
        return self.reg_c

    def run(self):
        while self.pointer < len(self.program) - 1:
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            instruction = self.instructions[opcode]
            self.pointer = instruction(operand)

        print(",".join([str(x) for x in self.output]))

    def adv(self, operand: int) -> int:
        """opcode 0"""
        operand = self.combo_operands[operand]()
        self.reg_a = self.reg_a//(2**operand)
        return self.pointer + 2

    def bxl(self, operand: int) -> int:
        """opcode 1"""
        self.reg_b = self.reg_b ^ operand
        return self.pointer + 2

    def bst(self, operand: int) -> int:
        """opcode 2"""
        operand = self.combo_operands[operand]()
        self.reg_b = operand % 8
        return self.pointer + 2

    def jnz(self, operand: int) -> int:
        """opcode 3"""
        if self.reg_a != 0:
            return operand

        return self.pointer + 2

    def bxc(self, _) -> int:
        """opcode 4"""
        self.reg_b = self.reg_b ^ self.reg_c
        return self.pointer + 2

    def out(self, operand: int) -> int:
        """opcode 5"""
        operand = self.combo_operands[operand]()
        self.output.append(operand % 8)
        return self.pointer + 2

    def bdv(self, operand: int) -> int:
        """opcode 6"""
        operand = self.combo_operands[operand]()
        self.reg_b = self.reg_a//(2**operand)
        return self.pointer + 2

    def cdv(self, operand: int) -> int:
        """opcode 7"""
        operand = self.combo_operands[operand]()
        self.reg_c = self.reg_a//(2**operand)
        return self.pointer + 2


def main():

    register_re = r"Register \w: (\d+)"

    with open("../inputs/day17_input.txt", encoding="utf-8") as f:
        lines = f.read().splitlines()
        reg_a = re.match(register_re, lines[0]).group(1)
        reg_b = re.match(register_re, lines[1]).group(1)
        reg_c = re.match(register_re, lines[2]).group(1)

        program = lines[4].replace("Program: ", "")

    p = Program(int(reg_a), int(reg_b), int(reg_c), program)
    p.run()


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")