from io import BytesIO,BufferedIOBase
from abc import ABC
from enum import IntEnum,Enum
class BaseInstruction(ABC):
    opcode:bytes
    def __init__(self,file:BufferedIOBase,exp:int) -> None:
        pass
class STKOp(IntEnum):
    get=0
    put=1
    sink=2
    float_=3
    lbl=4
    gl=5
class STKSTK(IntEnum):
    w=0
    sw=1
    e=2
    i=3
    st=4
    cs=5
    ps=6
    pis=7
class STK(BaseInstruction):
    opcode=b'\x01'
    def __init__(self,file:BufferedIOBase,exp:int=0):
        self.op:STKOp=int.from_bytes(file.read(1),signed=False)
        self.stk_:STKSTK=int.from_bytes(file.read(1),signed=False)
        self.arg:int=int.from_bytes(file.read(1+exp),signed=True)

class MDPOp(IntEnum):
    delete=0
    deleteall=1
    swap=2
    unlink=3
class MDP(BaseInstruction):
    opcode=b'\x02'
    def __init__(self,file:BufferedIOBase,exp:int=0):
        self.op: MDPOp =int.from_bytes(file.read(1),signed=False)

class UJMP(BaseInstruction):
    opcode=b'\x03'
    def __init__(self,file:BufferedIOBase,exp:int=0):
        self.loc: int =int.from_bytes(file.read(3+exp),signed=False)

class DSUB(BaseInstruction):
    opcode=b'\x04'
    def __init__(self,file:BufferedIOBase,exp:int=0):
        self.len: int =int.from_bytes(file.read(3+exp),signed=False)

class RETURN(BaseInstruction):
    opcode=b'\x05'
    def __init__(self,file:BufferedIOBase,exp:int=0): ...
class CALL(BaseInstruction):
    opcode=b'\x06'
    def __init__(self,file:BufferedIOBase,exp:int=0): ...
class SOPOp(IntEnum):
    add=0x00
    sub=0x01
    mult=0x02
    div=0x03
    modulo=0x04
    uneg=0x05
    band=0x06
    ubnot=0x07
    bor=0x08
    bnand=0x09
    bnor=0x0a
    bxor=0x0b
    bxnor=0x0c

class SOP(BaseInstruction):
    opcode=b'\x07'
    def __init__(self,file:BufferedIOBase,exp:int=0):
        self.op: SOPOp =int.from_bytes(file.read(3+exp),signed=False)
