from enum import Enum


class ObjectTypes(Enum):
    nil = 0
    boolean = 1
    number = 2
    table = 3


class InstructionType(Enum):
    move = "\x01"
    loadk = "\x02"
    loadbool = "\x03"
    loadnil = "\x04"
    jmp = "\x05"
    test = "\x06"  # if true execs next instr otherwise skip it


class ArditeInstruction:
    ...


class ArditeBytecodeHeader:
    arditemagic = "\x1bArd"
    ver = "\x00"
    #
    ...
