from io import BytesIO
from typing import Type
from .instructions import EXPMarkerInstruction, HitEOFException, instructions, Instruction, saferead
from enum import IntEnum, Enum

parserver = 0


class VMs(IntEnum):
    UNV = 0
    OFCPY = 1
    OFCLUA = 2
    OFCJS = 3


class BytecodeReaderException(Exception):
    ...


class VMStrs(Enum):
    UNV = b"UNV\x00\x00\x00\x00\x00"
    OFCPY = b"OFCPY\x00\x00\x00"
    OFCLUA = b"OFCLUA\x00\x00"
    OFCJS = b"OFCJS\x00\x00\x00"


class Bytecode:
    ver: int = 0
    vm: VMs | int = VMs.UNV
    vmstr: bytes = VMStrs.OFCPY.value
    instructions: list[Instruction] = []

    def __init__(self, f: BytesIO):
        # magi ver_ rawvm___
        if f.read(4) != b"\x1bSOL":
            raise Exception("Not a Sol Bytecode File")
        self.ver = int.from_bytes(saferead(f,4), signed=False)
        if self.ver != parserver:
            raise Exception(f"Cannot parse sol bytecode of version {self.ver} on parser version {parserver}")
        rawvm = saferead(f,8)
        self.vm = int.from_bytes(rawvm, signed=False)
        self.vmstr = rawvm
        exp = 0
        while True:
            byte = f.read(1)
            if not byte:
                break
            instr_cls: Type[Instruction] = instructions.get(int.from_bytes(byte, signed=False), None)
            if not instr_cls:
                continue
            try:
                instr = instr_cls.parse(f, exp)
                if isinstance(instr, EXPMarkerInstruction):
                    exp = instr.bytes_
                else:
                    self.instructions.append(instr)
                    exp = 0
            except HitEOFException:
                raise BytecodeReaderException("Hit EOF Early, is file intact?")
