# 1. GDB Baby Step 1

> Can you figure out what is in the `eax` register at the end of the `main` function? Put your answer in the picoCTF flag format: `picoCTF{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `picoCTF{17}`. Disassemble the given binary

## Solution:

From looking at the name of the challenge, we can immediately assume that we must use `gdb` for solving this. `gdb` is a popular cli debugger for C, C++ and more.

To launch gdb, we use:
```bash
gdb ./debugger0_a
```
Before doing this we must make sure to give the binary executable permissions using `chmod +x debugger0_a`.

The description also gives us another hint:
> Disassemble the given binary

The `disas` command in gdb is used to disassemble a binary into its individual assembly instructions. To disassemble the main function:
```console
(gdb) disas main
Dump of assembler code for function main:
   0x0000000000001129 <+0>:	endbr64
   0x000000000000112d <+4>:	push   %rbp
   0x000000000000112e <+5>:	mov    %rsp,%rbp
   0x0000000000001131 <+8>:	mov    %edi,-0x4(%rbp)
   0x0000000000001134 <+11>:	mov    %rsi,-0x10(%rbp)
   0x0000000000001138 <+15>:	mov    $0x86342,%eax
   0x000000000000113d <+20>:	pop    %rbp
   0x000000000000113e <+21>:	ret
End of assembler dump.
```

Before coming to the core of the problem, we must understand what the `eax` register, and before that, registers itself. Registers are special type of memory that is very fast and very small. They are built directly into the CPU, enabling their high speed. The `eax` register is often used to store the return values from functions.

In the output for `disas`, we see `mov $0x86342,%eax`, which means we are putting `0x86342` into `eax`. Converting it to decimal we get `549698`.

The above method is called `static analysis`, where you analyze the assembly instructions without running the program itself. The other method is `dynamic analysis`, and while in this example it does not really matter, we can use it as well.

`start` is used to enter into the main function frame and from there we can `disas` again. `start` starts running the program and creates a breakpoint on the first line of the main function and halts there for further instructions.
```console
(gdb) start
Temporary breakpoint 1 at 0x1131
Starting program: /home/gaurav/Projects/picogym/RevEngg/GDB_Baby_Step_1/debugger0_a 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Temporary breakpoint 1, 0x0000555555555131 in main ()
(gdb) disas
Dump of assembler code for function main:
   0x0000555555555129 <+0>:	endbr64
   0x000055555555512d <+4>:	push   %rbp
   0x000055555555512e <+5>:	mov    %rsp,%rbp
=> 0x0000555555555131 <+8>:	mov    %edi,-0x4(%rbp)
   0x0000555555555134 <+11>:	mov    %rsi,-0x10(%rbp)
   0x0000555555555138 <+15>:	mov    $0x86342,%eax
   0x000055555555513d <+20>:	pop    %rbp
   0x000055555555513e <+21>:	ret
End of assembler dump.
```

Using the address of the `ret` instruction (which is notably after we `mov` the value into `eax`), we can set a breakpoint at that location. Then, using `next` we can move to that breakpoint, then print the value stored in `eax`:
```console
(gdb) br *0x000055555555513e
Breakpoint 2 at 0x55555555513e
(gdb) next
Single stepping until exit from function main,
which has no line number information.

Breakpoint 2, 0x000055555555513e in main ()
(gdb) print $eax
$1 = 549698
```

Dynamic analysis is helpful in certain situations, for example when the value depends on user input perhaps (it won't be hardcoded in the assembly instructions).

## Flag:

```
picoCTF{549698}
```

## Concepts learnt:

- Assembly registers
- Working with `gdb`

## Notes:

- I also solved this using ghidra, using pretty much the same process of getting the assembly instruction.

## Resources:

- [GDB Basics Tutorial](https://youtu.be/MTkDTjdDP3c?si=KGEVArB0eDZJZSaA)
- [The disas command](https://primer.picoctf.org/#_example_of_execution_of_a_program)


***

# 2. Vault Door 3

> This vault uses for-loops and byte arrays. Reverse engineer it.

## Solution:

Here's the script i made to solve this:
```python
out = list("jU5t_a_sna_3lpm12g94c_u_4_m7ra41")
passwd = [""]*32

for i in range(31,16,-2):
    passwd[i] = out[i]
for i in range(16, 32, 2):
    passwd[46-i] = out[i]
for i in range(8,16):
    passwd[23-i]=out[i]
for i in range(8):
    passwd[i] = out[i]

print("".join(passwd))

```

Output:
```
jU5t_a_s1mpl3_an4gr4m_4_u_c79a21
```

The main principle in this solution is that VaultDoor3.java takes in a password, and runs a special "encryption" (a bunch of operations on certain sections of the password). To get the password we must reverse engineer these operations and work our way backwards. The rest is pretty much self explanatory.

## Flag:

```
picoCTF{jU5t_a_s1mpl3_an4gr4m_4_u_c79a21}
```

## Notes:
None

## Resources:
None

***

# 3. ARMssembly 1

> For what argument does this program print `win` with variables `83`, `0` and `3`? File: [chall_1.S](https://mercury.picoctf.net/static/b4fd1dabc9dec63c37180b5b05783b55/chall_1.S) Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

## Solution:

`chall_1.S` is an assembly source file. You can attempt this in multiple ways, but probably the easiest way is to convert it into C code. Putting chall_1.S in an online converter, we get:
```C
#include <stdio.h>
#include <stdlib.h>

int func(int w0) {
    int var_12 = w0;
    int var_16 = 83;
    int var_20 = 0;
    int var_24 = 3;
    int var_28;

    var_28 = var_16 << var_20;
    var_28 = var_28 / var_24;
    var_28 = var_28 - var_12;

    return var_28;
}

int main(int argc, char **argv) {
    int input = atoi(argv[1]);
    int result = func(input);

    if (result == 0) {
        puts("You win!");
    } else {
        puts("You Lose :(");
    }

    return 0;
}
```
For us to get our win condition, the function `func` must return 0. Going through the code, `var_12` is our input, `var_16`, `var_20`, `var_24` are integer constants and `var_28` is what we will be returning.
- `var_28` = `var_16` << `var_20` = 83 << 0 = 83 (left shifting by `0` bits)
- `var_28` = `var_28` / `var_24` = 83 / 3 = 27
- `var_28` = `var_28` - `var_12` = 27 - `input`
- Since `var_28` must be equal to 0, `input`= 27
- 27 in hex is `1B`, when adjusted to meet the requirements, the flag is:
## Flag:

```
picoCTF{0000001b}
```

## Concepts learnt:

- Converting assembly source files

## Notes:

- None

## Resources:

- [Converter](https://www.codeconvert.ai/assembly-to-c-converter)


***

