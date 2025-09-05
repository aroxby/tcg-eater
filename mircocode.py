#!/usr/bin/env python3
"""
The goal here is to output readable assembly that can be used for microcode
"""
from enum import Enum, IntEnum


HEADER = "# Memory layout: 0xABCD where A is 0 (reserved), B is the flags, C is the opcode, D is the step number"


MAX_STEPS = 15


class OpCodes(IntEnum):
    NOP = 0x0
    LDA = 0x1
    ADD = 0x2
    SUB = 0x3
    STA = 0x4
    LDI = 0x5
    JMP = 0x6
    JC  = 0x7
    JZ  = 0x8
    OUT = 0xE
    HLT = 0xF


class Signals(Enum):
    HLT = "001"
    MRI = "002"
    RMI = "004"
    RMO = "008"
    IRI = "016"
    IRO = "032"
    ARI = "064"
    ARO = "128"
    SRO = "001*256"
    SUB = "002*256"
    BRI = "004*256"
    ORI = "008*256"
    PCE = "016*256"
    PCO = "032*256"
    PCI = "064*256"
    FLU = "128*256"
    NOP = "0"


# For easier typing, create local variables for signal values
for signal in Signals: locals()[signal.name] = signal.name


BASE_STEPS = [[MRI, PCO, PCE], [RMO, IRI]]
MICROCODE = {
    OpCodes.NOP: BASE_STEPS,
    OpCodes.LDA: BASE_STEPS + [[IRO, MRI], [RMO, ARI]],
    OpCodes.ADD: BASE_STEPS + [[IRO, MRI], [RMO, BRI], [SRO, ARI, FLU]],
    OpCodes.SUB: BASE_STEPS + [[IRO, MRI], [RMO, BRI], [SUB, SRO, ARI, FLU]],
    OpCodes.STA: BASE_STEPS + [[IRO, MRI], [ARO, RMI]],
    OpCodes.LDI: BASE_STEPS + [[IRO, ARI]],
    OpCodes.JMP: BASE_STEPS + [[IRO, PCI]],
    OpCodes.JC: BASE_STEPS,
    OpCodes.JZ: BASE_STEPS,
    OpCodes.OUT: BASE_STEPS + [[ARO, ORI]],
    OpCodes.HLT: BASE_STEPS + [[HLT]],
}


longest_instruction = max(len(code) for code in MICROCODE.values())
assert longest_instruction <= MAX_STEPS


output = HEADER + "\n"
for signal in Signals:
    output += f"const {signal.name} {signal.value}\n"

for zf in (0, 1):
    for cf in (0, 1):
        for opcode in range(max(OpCodes) + 1):
            try:
                op = OpCodes(opcode)
                name = op.name
                microcode = MICROCODE[op]
            except ValueError:
                name = "Undefined"
                microcode = MICROCODE[OpCodes.NOP]

            if (opcode == OpCodes.JC and cf == 1) or (opcode == OpCodes.JZ and zf == 1):
                microcode = MICROCODE[OpCodes.JMP]

            address = zf << 9 | cf << 8 | opcode << 4
            output += f"\n# {address:04X} {name}({opcode:X}),CF={cf},ZF={zf}\n"

            for step in range(MAX_STEPS + 1):
                try:
                    step_code = microcode[step]
                except IndexError:
                    step_code = (NOP,)
                output += "+".join(step_code) + "\n"

print(output)
