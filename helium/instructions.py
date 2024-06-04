from enum import IntEnum
from io import BytesIO
from typing import Self


class ObjectTypes(IntEnum):
    nil = 0x0
    boolean = 0x1
    number = 0x2
    table = 0x3


class HitEOFException(Exception):
    ...


def saferead(f: BytesIO, size: int):
    e = f.read(size)
    if len(e) != size:
        raise HitEOFException(
            f"Hit EOF in read of {size} bytes, got {len(e)}"
            f" ( {' '.join([hex(b)[2:].upper() for b in e])} EOF )"
        )
    return e


class InstructionType(IntEnum):
    stk = 0x1
    mpd = 0x2
    ujmp = 0x3
    dsub = 0x4
    return_ = 0x5
    call = 0x6
    sop = 0x7
    const = 0x8
    exp = 0x9


class Instruction:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__("k", v)

    @classmethod
    def parse(cls, file: BytesIO, exp) -> Self:
        return cls()


class STK_op(IntEnum):
    get = 0x0
    put = 0x1
    sink = 0x2
    float_ = 0x3
    lbl = 0x4
    gl = 0x5


class STK_stk(IntEnum):
    w = 0x0
    sw = 0x1
    e = 0x2
    i = 0x3
    st = 0x4
    cs = 0x5
    ps = 0x6
    pis = 0x7
    pls = 0x8


class STKInstruction(Instruction):
    op: STK_op
    stk: STK_stk
    arg: int

    @classmethod
    def parse(cls, file: BytesIO, exp):
        op = int.from_bytes(saferead(file, 1), signed=False)
        stk = int.from_bytes(saferead(file, 1), signed=False)
        arg = None
        if op in [STK_op.get, STK_op.put, STK_op.sink, STK_op.float_,]:
            arg = int.from_bytes(saferead(file, 1), signed=(op in [STK_op.sink, STK_op.float_]))
        return cls(op=op, stk=stk, arg=arg)


class MDP_op(IntEnum):
    delete = 0x0
    deleteall = 0x1
    swap = 0x2
    unlink = 0x3
    setall = 0x4


class MDPInstruction(Instruction):
    op: MDP_op

    @classmethod
    def parse(cls, file: BytesIO, exp):
        op = int.from_bytes(saferead(file, 1), signed=False)
        return cls(op=op)


class UJMPInstruction(Instruction):
    loc: int

    @classmethod
    def parse(cls, file: BytesIO, exp):
        loc = int.from_bytes(saferead(file, 3 + exp), signed=False)
        return cls(loc=loc)


class DSUBInstruction(Instruction):
    len_: int

    @classmethod
    def parse(cls, file: BytesIO, exp):
        len_ = int.from_bytes(saferead(file, 3 + exp), signed=False)
        return cls(len_=len_)


class RETURNInstruction(Instruction):
    ...


class CALLInstruction(Instruction):
    ...


class SOP_op(IntEnum):
    add = 0x00
    sub = 0x01
    mult = 0x02
    div = 0x03
    modulo = 0x04
    uneg = 0x05
    band = 0x07
    ubnot = 0x08
    bor = 0x09
    bnand = 0x0a
    bnor = 0x0b
    bxor = 0x0c
    bxnor = 0x0d
    eqv = 0x0e
    se = 0x0f
    is_ = 0x10
    gte = 0x11
    lte = 0x12
    gee = 0x13
    lee = 0x14
    gt = 0x15
    lt = 0x16
    ge = 0x17
    le = 0x18
    ne = 0x19
    nee = 0x1a


class SOPInstruction(Instruction):
    op: SOP_op

    @classmethod
    def parse(cls, file: BytesIO, exp):
        op = int.from_bytes(saferead(file, 1), signed=False)
        return cls(op=op)


class CONST_typ(IntEnum):
    int_ = 0x0
    float_ = 0x1
    str_ = 0x2
    bool_ = 0x3
    nil = 0x4


class CONSTInstruction(Instruction):
    typ: CONST_typ
    len_: int
    data: int | float | str | bool | None

    @classmethod
    def parse(cls, file: BytesIO, exp):
        typ = int.from_bytes(saferead(file, 1), signed=False)
        len_ = int.from_bytes(saferead(file, 2 + exp), signed=False)
        match typ:
            case 0:
                data = int.from_bytes(saferead(file, len_))
            case 1:
                data = float(saferead(file, len_).decode("ascii"))  # just parse from string, because idk a better way
            case 2:
                data = saferead(file, len_).decode("ascii")
            case 3:
                data = bool(int.from_bytes(saferead(file, 1)) & 0x80)
                len_ = 1
            case 4:
                data = None
                len_ = 0
            case _:
                data = None
                print(f"Unexpected CONST type: {typ}. just using none")
        return cls(typ=typ, len_=len_, data=data)


class EXPMarkerInstruction(Instruction):
    bytes_: int

    @classmethod
    def parse(cls, file: BytesIO, exp):
        return cls(bytes_=int.from_bytes(saferead(file, 1 + exp), signed=False))


instructions = {
    0x1: STKInstruction,
    0x2: MDPInstruction,
    0x3: UJMPInstruction,
    0x4: DSUBInstruction,
    0x5: RETURNInstruction,
    0x6: CALLInstruction,
    0x7: SOPInstruction,
    0x8: CONSTInstruction,
    0x9: EXPMarkerInstruction,
}
