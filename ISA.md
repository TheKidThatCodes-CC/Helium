# Instruction Set/Architecture
Sol, unlike lua, is purely stack based instead of register based. I will try to keep this instruction set small so that it is easy to comprehend.

Working data piece (wdp)
Operating data piece (odp)

### stk
args: op[8bit] stk[8bit]
- op:
    - get[0x00]
      gets from top of stack and puts it into (wdp)
    - put[0x01]
      puts (wdp) on top of the stack
    - sink[0x2]
      makes the value on top of the stack sink pl{8bit} places or if the MSB of pl is on then it takes it to the place relative to the bottom
    - float[0x3]
      makes the value at {pl} from the top (or bottom if MSB on) float to the top of the stack
    - lbl[0x4]
      labels the top stack item with (wdp)
    - gl[0x5]
      copies the label f
