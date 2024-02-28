# Instruction Set/Architecture
Sol, unlike lua, is purely stack based instead of register based. I will try to keep this instruction set small so that it is easy to comprehend.

Working data piece (wdp)
Operating data piece (odp)

### - **stk**
- op[8bit] stk[8bit] {arg[8bit]}
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
      makes the value at arg from the top (or bottom if MSB on) float to the top of the stack
    - lbl[0x4]<br>
      labels the top stack item with (wdp)
    - gl[0x5]<br>
      puts pointer of the label from top of stack to (wdp)
  - stk:
    - w[0x00]<br>
    the current working stack
    - e[0x01]<br>
    the stack that is exported by return or calling a function
    - i[0x02]<br>
    the recived e stack
    - st[0x03]<br>
    substack tree<br>
    can only have pointers<br>
    can only get and put, sink is delete top
    - cs[0x04]<br>
    current substack (from st)
    - ps[0x05]<br>
    all accessible things from parent w stacks (used for closures)
    - pis[0x06]<br>
    ps but i stacks

