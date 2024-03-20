# Instruction Set/Architecture
Sol, unlike lua, is purely stack based instead of register based. I will try to keep this instruction set small so that it is easy to comprehend.

Working data piece (wdp)
Operating data piece (odp)

- ### **stk**  op[8bit] stk[8bit] {arg[8bit]}
  - op:
    - get[0x00]
      gets from top of stack and puts it into (wdp)<br>
      arg:
      - 0x00: takes it from stack
      - 0x01: copies pointer
      - 0x02: copies
    - put[0x01]
      puts (wdp) on top of the stack<br>
      arg:
      - 0x00: put it on to stack
      - 0x01: puts pointer on to stack
      - 0x02: copies onto stack
    - sink[0x2]
      makes the value on top of the stack sink arg places or if the MSB of arg is on then it takes it to the place relative to the bottom
    - float[0x3]
      makes the value at arg from the top (or bottom if MSB on) float to the top of the stack<br>
      if multiple with same label makes them all float in their current order
    - lbl[0x4]<br>
      labels the top stack item with (wdp)
    - gl[0x5]<br>
      puts pointer of the label from top of stack to (wdp)
  - stk:
    - w[0x00]<br>
    the current working stack
    - sw[0x01]<br>
    the secondairy working stack, only accessible from its own scope, does not pass to parent or child
    - e[0x02]<br>
    the stack that is exported by return or calling a function
    - i[0x03]<br>
    the recived e stack
    - st[0x04]<br>
    substack tree<br>
    can only have pointers<br>
    can only get and put, sink is delete top,float delets everything above
    - cs[0x05]<br>
    current substack (from st)
    - ps[0x06]<br>
    all accessible things from parent w stacks (used for closures)
    - pis[0x07]<br>
    ps but i stacks
- ### **mdp** op[8bit]
  - op:
    - delete[0x00]
      <br>
      deletes the current reference, if it is the last one then object is deleted
    - deleteall [0x01]
      <br>
      deletes all references and object
    - swap[0x02]
      <br>
      swaps wdp and odp
    - unlink[0x03]
      <br>
      detatches object from all other references (essentially copy but whatever)
- ### **ujmp** loc[exp(24bit)]
  <br>
  Jumps to instruction
- ### **dsub** len[exp(24bit)]
  <br>
  defines a subroutine (function) len instructions long and places it on the stack, as well as removing the instructions that make up the function from the code, so watch out using jumps
- ### **return**
  returns the e stack and jumps back to after call
- ### **call**
  takes the function, puts in in sw stack, then calls it
- ### **sop** op[8bit]
  does: wdp op odp. or if its unary it just does it on wdp
  puts result on top of wstack
  - op:
    - add[0x00]
    - sub[0x01]
    - mult[0x02]
    - div[0x03]
    - modulo[0x04]
    - unary negation[0x05]
    - bitwise and[0x07]
    - unary bitwise not[0x08]
    - bitwise or[0x09]
    - bitwise nand[0x0a]
    - bitwise nor[0x0b]
    - bitwise xor[0x0c]
    - bitwise xnor[0x0d]
- ### **const** typ[4bit] len[exp(16bit)+4bit]
  reads len bytes after the instruction and puts it on w stack, then goes past any 0x00 s untill it gets to the next instruction
  - typ:
    - int[0x00] top bit is sign
    - float[0x01] probably platform specific
    - str[0x02] simple
    - bool[0x03] first bit?
    - null/nil/none[0x04]
- ### **exp** bytes[exp(8bit)]
  makes the size of the exp() field in the next instruction bytes bytes long, this is a marker, not a actual instruction. this
