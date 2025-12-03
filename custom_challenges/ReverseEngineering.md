# 1. JoyDivision

## Solution:

Using IDA free, I disassembled the binary and decompiled it. Here are the relevant functions:
```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned __int64 len_plus_15; // rax
  void *v4; // rsp
  char v6[8]; // [rsp+8h] [rbp-80h] BYREF
  int i; // [rsp+10h] [rbp-78h]
  int length; // [rsp+14h] [rbp-74h]
  FILE *stream; // [rsp+18h] [rbp-70h]
  __int64 len_minus_one; // [rsp+20h] [rbp-68h]
  char *s; // [rsp+28h] [rbp-60h]
  __int64 v12; // [rsp+30h] [rbp-58h]
  __int64 v13; // [rsp+38h] [rbp-50h]
  void *ptr; // [rsp+40h] [rbp-48h]
  FILE *v15; // [rsp+48h] [rbp-40h]
  unsigned __int64 v16; // [rsp+50h] [rbp-38h]

  v16 = __readfsqword(0x28u);
  puts("\nMay Jupiter strike you down Caeser before you seize the treasury!! You will have to tear me apart");
  puts("for me to tell you the flag to unlock the Roman Treasury and fund your civil war. I, Lucius Caecilius");
  puts("Metellus, shall not let you pass until you get this password right. (or threaten to kill me-)\n");
  stream = fopen("palatinepackflag.txt", "r");
  fseek(stream, 0LL, 2);
  length = ftell(stream) + 1;
  fseek(stream, 0LL, 0);
  len_minus_one = length - 1LL;
  len_plus_15 = 16 * ((length + 15LL) / 0x10uLL);
  while ( v6 != &v6[-(len_plus_15 & 0xFFFFFFFFFFFFF000LL)] )
    ;
  v4 = alloca(len_plus_15 & 0xFFF);
  if ( (len_plus_15 & 0xFFF) != 0 )
    *(_QWORD *)&v6[(len_plus_15 & 0xFFF) - 8] = *(_QWORD *)&v6[(len_plus_15 & 0xFFF) - 8];
  s = v6;
  fgets(v6, length, stream);
  flipBits(s, (unsigned int)length);
  v12 = expand(s, (unsigned int)length);
  v13 = expand(v12, (unsigned int)(2 * length));
  ptr = (void *)expand(v13, (unsigned int)(4 * length));
  anti_debug();
  for ( i = 0; i < 8 * length; ++i )
    putchar(*((unsigned __int8 *)ptr + i));
  putchar(10);
  v15 = fopen("flag.txt", "wb");
  fwrite(ptr, 1uLL, 8 * length, v15);
  fclose(v15);
  return 0;
}
```

```c
__int64 __fastcall flipBits(__int64 a1, int a2)
{
  __int64 result; // rax
  char v3; // [rsp+13h] [rbp-9h]
  _BOOL4 v4; // [rsp+14h] [rbp-8h]
  unsigned int i; // [rsp+18h] [rbp-4h]

  v4 = 0;
  v3 = 105;
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( (int)i >= a2 )
      break;
    if ( v4 )
    {
      *(_BYTE *)((int)i + a1) ^= v3;
      v3 += 32;
    }
    else
    {
      *(_BYTE *)((int)i + a1) = ~*(_BYTE *)((int)i + a1);
    }
    v4 = !v4;
  }
  return result;
}

```

```c
_BYTE *__fastcall expand(__int64 a1, int a2)
{
  unsigned __int8 v3; // [rsp+1Bh] [rbp-15h]
  _BOOL4 v4; // [rsp+1Ch] [rbp-14h]
  int i; // [rsp+20h] [rbp-10h]
  _BYTE *v6; // [rsp+28h] [rbp-8h]

  v4 = 0;
  v3 = 105;
  v6 = malloc(2 * a2);
  for ( i = 0; i < a2; ++i )
  {
    if ( v4 )
    {
      v6[2 * i] = (v3 >> 4) | *(_BYTE *)(i + a1) & 0xF0;
      v6[2 * i + 1] = (16 * v3) | *(_BYTE *)(i + a1) & 0xF;
    }
    else
    {
      v6[2 * i] = (16 * v3) | *(_BYTE *)(i + a1) & 0xF;
      v6[2 * i + 1] = (v3 >> 4) | *(_BYTE *)(i + a1) & 0xF0;
    }
    v3 *= 11;
    v4 = !v4;
  }
  printf("fie");
  return v6;
}

```

```c
void anti_debug()
{
    if (ptrace(0, 0, 1, 0) != -1)
        return;
    puts("THOU SHALL NOT READ MY MIND WITH GOTHIC MAGIC CAESER!!!\n");
    exit(1); /* do not return */
}
```


Following the logic, I made this program to decompile it:
```python
flag_file = open("flag.txt", "rb")
flag = flag_file.read()
flag = bytearray(flag)

def de_expand(arr):
    og_arr = bytearray(len(arr) // 2)
    v3 = 105
    v4 = False
    
    for i in range(len(og_arr)):
        byte1 = arr[2 * i]
        byte2 = arr[2 * i + 1]
        
        if v4:
            og_arr[i] = (byte1 & 0xF0) | (byte2 & 0x0F)
        else:
            og_arr[i] = (byte1 & 0x0F) | (byte2 & 0xF0)
        
        v3 = (v3 * 11) % 256 
        # Lost a lot of hair before figuring out v3 was an 8bit/1 byte integer in the decompiled C code. fml.
        v4 = not v4
    
    return og_arr

def de_flipbits(arr):
    v4 = False
    v3 = 105;
    
    for i in range(len(arr)):
        if v4:
            arr[i] = arr[i] ^ v3
            v3 = (v3 + 32 ) % 256
        else:
            arr[i] = (~arr[i]) & 0xFF 
            # this & 0xFF bullshit is fucking stupid fuck python
        v4 = not v4

    return arr

del flag[len(flag) - 1]
v13 = de_expand(flag)
v12 = de_expand(v13)
s = de_expand(v12)
s = de_flipbits(s)

print(s)
print(s.decode())
```

Few points of interest:
- in `de_expand`, v3 is an unsigned 8bit integer, but python uses infinite precision, so to simulate integer overflow we have to `% 256`.
- again, because be are using Python which has infinite precision, we have to `& 0xFF` in `de_flipbits` to disregard the sign bit.

## Flag:

```
sunshine{C3A5ER_CR055ED_TH3_RUB1C0N}
```

## Concepts learnt:

- Reinforced existing concepts and the process of reverse engineering.
- Learnt about how stack memory management works, how the kernel allocates memory in 4kb chunks, and how the compiler inserts code to page each of those chunks before any of it used.

## Notes:

- A lot of time was sent on figuring out which parts of the decompiled code were the actual logic from the original code, and which parts were inserted by the compiler for memory management.


***

# 2. worthy.knight

## Solution:

The first think I did was look up what a .knight extension is, which came back to be the encrypted output of the Knight ransomware. Seeing as how no way of decrypting it without a key exists, I disregarded this fact.

Decompiling it, here are the relevant functions:
```c

undefined4 FUN_001010d0(void)

{
   byte bVar1;
   int iVar2;
   char *null_check;
   size_t length;
   ushort **ppuVar3;
   byte *input_copy;
   undefined4 uVar4;
   char *pcVar5;
   long in_FS_OFFSET;
   ushort local_10c;
   undefined1 local_10a;
   byte local_108 [16];
   char local_f8 [32];
   char local_d8 [16];
   undefined1 input [16];
   undefined1 local_b8 [16];
   undefined1 local_a8 [16];
   undefined1 local_98 [16];
   undefined1 local_88 [16];
   undefined1 local_78 [16];
   undefined1 local_68 [16];
   undefined1 local_58 [16];
   long local_40;
   ushort input0;
   ushort input1;
   
   local_40 = *(long *)(in_FS_OFFSET + 0x28);
   puts(
         "                       (Knight\'s Adventure)                \n\n         O                                              \n        <M>            .---.                            \n        /W\\           ( -.- )--------.                  \n   ^    \\|/            \\_o_/         )    ^             \n  /|\\    |     *      ~~~~~~~       /    /|\\            \n  / \\   / \\  / |\\                    /    / \\            \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~\nWelcome, traveler. A mighty dragon blocks the gate.\nSpeak the secret incantation ( 10 runic letters) to continue.\n"
         );
   input = (undefined1  [16])0x0;
   local_b8 = (undefined1  [16])0x0;
   local_a8 = (undefined1  [16])0x0;
   local_98 = (undefined1  [16])0x0;
   local_88 = (undefined1  [16])0x0;
   local_78 = (undefined1  [16])0x0;
   local_68 = (undefined1  [16])0x0;
   local_58 = (undefined1  [16])0x0;
   printf("Enter your incantation: ");
   null_check = fgets(input,0x80,stdin);
   if (null_check == (char *)0x0) {
      puts("\nSomething went awry. Fare thee well...");
   }
   else {
      length = strcspn(input,"\n");
      input[length] = 0;
      length = strlen(input);
      if (length == 10) {
         ppuVar3 = __ctype_b_loc();
         input_copy = input;
         do {
            input0 = (*ppuVar3)[*input_copy];
            if (((input0 & 0x400) == 0) || (input1 = (*ppuVar3)[input_copy[1]], (input1 & 0x400) == 0))
            {
               puts("\nThe runes fail to align. The incantation is impure.");
               puts(&DAT_001022b8);
               goto LAB_0010124c;
            }
            if ((((input0 & 0x100) != 0) && ((input1 & 0x100) != 0)) ||
                 (((input0 & 0x200) != 0 && ((input1 & 0x200) != 0)))) {
               puts("\nThe ancient seals do not resonate with your runes.");
               puts(&DAT_001022b8);
               goto LAB_0010124c;
            }
            input_copy = input_copy + 2;
         } while (input_copy != input + 10);
         if ((byte)(input[1] ^ input[0]) == 0x24) {
            if (input[1] == 0x6a) {
               if ((input[2] ^ input[3]) == 0x38) {
                  if (input[3] == 0x53) {
                      local_10a = 0;
                      input_copy = local_108;
                      local_10c = input._4_2_ << 8 | (ushort)input._4_2_ >> 8;
                      length = strlen((char *)&local_10c);
                      MD5((uchar *)&local_10c,length,input_copy);
                      null_check = local_f8;
                      do {
                         bVar1 = *input_copy;
                         pcVar5 = null_check + 2;
                         input_copy = input_copy + 1;
                         sprintf(null_check,"%02x",(ulong)bVar1);
                         null_check = pcVar5;
                      } while (local_d8 != pcVar5);
                      local_d8[0] = '\0';
                      iVar2 = strcmp(local_f8,"33a3192ba92b5a4803c9a9ed70ea5a9c");
                      if (iVar2 == 0) {
                         if ((input[6] ^ input[7]) == 0x38) {
                            if (input[7] == 0x61) {
                               if ((byte)(input[9] ^ input[8]) == 0x20) {
                                  if (input[9] == 0x69) {
                                     printf("\n%s\n",
                                                "   The kingdom\'s gates open, revealing the hidden realm...    \n                         ( (                                 \n                          \\ \\                                \n                     .--.  ) ) .--.                         \n                    (    )/_/ (    )                        \n                     \'--\'       \'--\'                         \n    \"Huzzah! Thy incantation is true. Onward, brave knight!\" \n"
                                               );
                                     printf("The final scroll reveals your reward: KCTF{%s}\n\n",input);
                                     uVar4 = 0;
                                     goto LAB_00101251;
                                  }
                                  puts("\nThe wards reject your Pair 5 second char.");
                                  puts(&DAT_001022b8);
                               }
                               else {
                                  puts("\nThe wards reject your Pair 5.");
                                  puts(&DAT_001022b8);
                               }
                            }
                            else {
                               puts("\nThe wards reject your Pair 4 second char.");
                               puts(&DAT_001022b8);
                            }
                         }
                         else {
                            puts("\nThe wards reject your Pair 4.");
                            puts(&DAT_001022b8);
                         }
                      }
                      else {
                         puts("\nThe dragon\'s eyes glow red... The final seal remains locked.");
                         puts(&DAT_001022b8);
                      }
                  }
                  else {
                      puts("\nThe wards reject your Pair 2 second char.");
                      puts(&DAT_001022b8);
                  }
               }
               else {
                  puts("\nThe wards reject your Pair 2.");
                  puts(&DAT_001022b8);
               }
            }
            else {
               puts("\nThe wards reject your Pair 1 second char.");
               puts(&DAT_001022b8);
            }
         }
         else {
            puts("\nThe wards reject your Pair 1.");
            puts(&DAT_001022b8);
         }
      }
      else {
         puts("\nScribe\'s note: The incantation must be exactly 10 runic symbols.");
         puts(&DAT_001022b8);
      }
   }
LAB_0010124c:
   uVar4 = 1;
LAB_00101251:
   if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
      return uVar4;
   }
                               /* WARNING: Subroutine does not return */
   __stack_chk_fail();
}
```

This was an interesting solve, requiring multiple separate programs. I have also renamed some of the variables in Ghidra (I got sick of IDA) to make it more readable based on the logic.

This program seems to take in user input, and checks each pair of character with a whole bunch of rules. the first rule is that the user input must be 10 characters long.

The program is using <ctype.h> which has a lookup table for each character with an integer, where each bit is a result of functions like `isDigit()`, `isAlpha()`, `isPunctuation()`. We then perform `&` operation on that integer to get each bit result. Looking at `/usr/include/ctype.h`:
```c
#ifndef _ISbit
/* These are all the characteristics of characters.
   If there get to be more than 16 distinct characteristics,
   many things must be changed that use `unsigned short int's.

   The characteristics are stored always in network byte order (big
   endian).  We define the bit value interpretations here dependent on the
   machine's byte order.  */

# include <bits/endian.h>
# if __BYTE_ORDER == __BIG_ENDIAN
#  define _ISbit(bit)	(1 << (bit))
# else /* __BYTE_ORDER == __LITTLE_ENDIAN */
#  define _ISbit(bit)	((bit) < 8 ? ((1 << (bit)) << 8) : ((1 << (bit)) >> 8))
# endif

enum
{
  _ISupper = _ISbit (0),	/* UPPERCASE.  */
  _ISlower = _ISbit (1),	/* lowercase.  */
  _ISalpha = _ISbit (2),	/* Alphabetic.  */
  _ISdigit = _ISbit (3),	/* Numeric.  */
  _ISxdigit = _ISbit (4),	/* Hexadecimal numeric.  */
  _ISspace = _ISbit (5),	/* Whitespace.  */
  _ISprint = _ISbit (6),	/* Printing.  */
  _ISgraph = _ISbit (7),	/* Graphical.  */
  _ISblank = _ISbit (8),	/* Blank (usually SPC and TAB).  */
  _IScntrl = _ISbit (9),	/* Control character.  */
  _ISpunct = _ISbit (10),	/* Punctuation.  */
  _ISalnum = _ISbit (11)	/* Alphanumeric.  */
};
#endif /* ! _ISbit  */
```

from this we can see which function corresponds to which mask value for the `&` operation.

From this line:
`if (((input0 & 0x400) == 0) || (input1 = (*ppuVar3)[input_copy[1]], (input1 & 0x400) == 0))`, this line checks if every character is an alphabet
this line, `if ((((input0 & 0x100) != 0) && ((input1 & 0x100) != 0)) || (((input0 & 0x200) != 0 && ((input1 & 0x200) != 0))))` checks if each pair of characters is of opposite case.

If we pass these two rules, we move on to the individual character testing:
`if ((byte)(input[1] ^ input[0]) == 0x24)`, this line says the XOR of the bits of the 1st and second character must be 0x24. To find pairs of such characters, I made this script:
```python
mask = int(input("Enter mask integer: "), 16)

for i in range(65, 91):
    char1 = chr(i)
    for j in range(97, 123):
        char2 = chr(j)
        if i ^ j == mask:
            print(f"char1: {char1}\nchar2: {char2}")
    print("======")
```
I won't include the output for the sake of brevity, but this gives me each character pair that satisfies the XOR condition.
We see from this line that `if (input[1] == 0x6a)`, the second character must correspond to the ASCII value of `106`, which is `j`. Looking at the output of pairfinder.py, we can find the corresponding character.

Repeating this for all the other characters (except for 5 and 6), we get the following input phrase:
`NjkS__YaIi`, where `__` can be any character. In the decompiled code, they are performing some bit operations then taking the MD5 hash of the output and comparing it. Being completely honest, I don't feel like following those operations, so I decided to bruteforce it, since its only 2 characters. I made a script to do so:
```python
import subprocess

alpha = "abcdefghijklmnopqrstuvwxyz"

for upper in alpha.upper():
    for lower in alpha:
        result = subprocess.run(["./worthy.knight"], input=f"NjkS{lower}{upper}YaIi", capture_output=True, text=True)
        if "KCTF" in result.stdout.upper():
            print(f"NjkS{lower}{upper}YaIi")
            exit()
```

Running this we get the flag.

## Flag:

```
KCTF{NjkSfTYaIi}
```

***
# 3. time
## Solution:

Since we are using a random number generator, we can't really find the flag using just decompilation since the number is being generated at runtime. Therefore we use a debugger:
```c
gdb ./time
GNU gdb (GDB) 16.3
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./time...

This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.archlinux.org>
Enable debuginfod for this session? (y or [n]) y
Debuginfod has been enabled.
To make this setting permanent, add 'set debuginfod enabled on' to .gdbinit.
(No debugging symbols found in ./time)
(gdb) start
Temporary breakpoint 1 at 0x40092f
Starting program: /home/gaurav/Projects/gaurav_phase2/custom_challenges/RevEngg/time/time 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Temporary breakpoint 1, 0x000000000040092f in main ()
(gdb) disas
Dump of assembler code for function main:
   0x000000000040092b <+0>:	push   %rbp
   0x000000000040092c <+1>:	mov    %rsp,%rbp
=> 0x000000000040092f <+4>:	sub    $0x20,%rsp
   0x0000000000400933 <+8>:	mov    %edi,-0x14(%rbp)
   0x0000000000400936 <+11>:	mov    %rsi,-0x20(%rbp)
   0x000000000040093a <+15>:	mov    %fs:0x28,%rax
   0x0000000000400943 <+24>:	mov    %rax,-0x8(%rbp)
   0x0000000000400947 <+28>:	xor    %eax,%eax
   0x0000000000400949 <+30>:	mov    $0x0,%edi
   0x000000000040094e <+35>:	call   0x400750 <time@plt>
   0x0000000000400953 <+40>:	mov    %eax,%edi
   0x0000000000400955 <+42>:	call   0x400730 <srand@plt>
   0x000000000040095a <+47>:	call   0x400790 <rand@plt>
   0x000000000040095f <+52>:	mov    %eax,-0xc(%rbp)
   0x0000000000400962 <+55>:	lea    0x1c7(%rip),%rdi        # 0x400b30
   0x0000000000400969 <+62>:	call   0x4006e0 <puts@plt>
   0x000000000040096e <+67>:	lea    0x1e3(%rip),%rdi        # 0x400b58
   0x0000000000400975 <+74>:	call   0x4006e0 <puts@plt>
   0x000000000040097a <+79>:	lea    0x207(%rip),%rdi        # 0x400b88
   0x0000000000400981 <+86>:	call   0x4006e0 <puts@plt>
   0x0000000000400986 <+91>:	lea    0x21b(%rip),%rdi        # 0x400ba8
   0x000000000040098d <+98>:	mov    $0x0,%eax
   0x0000000000400992 <+103>:	call   0x400710 <printf@plt>
   0x0000000000400997 <+108>:	mov    0x2006ea(%rip),%rax        # 0x601088 <stdout@@GLIBC_2.2.5>
   0x000000000040099e <+115>:	mov    %rax,%rdi
   0x00000000004009a1 <+118>:	call   0x400760 <fflush@plt>
   0x00000000004009a6 <+123>:	lea    -0x10(%rbp),%rax
   0x00000000004009aa <+127>:	mov    %rax,%rsi
   0x00000000004009ad <+130>:	lea    0x208(%rip),%rdi        # 0x400bbc
   0x00000000004009b4 <+137>:	mov    $0x0,%eax
   0x00000000004009b9 <+142>:	call   0x400780 <__isoc99_scanf@plt>
   0x00000000004009be <+147>:	mov    -0x10(%rbp),%eax
   0x00000000004009c1 <+150>:	mov    %eax,%esi
   0x00000000004009c3 <+152>:	lea    0x1f5(%rip),%rdi        # 0x400bbf
   0x00000000004009ca <+159>:	mov    $0x0,%eax
   0x00000000004009cf <+164>:	call   0x400710 <printf@plt>
   0x00000000004009d4 <+169>:	mov    -0xc(%rbp),%eax
   0x00000000004009d7 <+172>:	mov    %eax,%esi
   0x00000000004009d9 <+174>:	lea    0x1f3(%rip),%rdi        # 0x400bd3
   0x00000000004009e0 <+181>:	mov    $0x0,%eax
   0x00000000004009e5 <+186>:	call   0x400710 <printf@plt>
   0x00000000004009ea <+191>:	mov    0x200697(%rip),%rax        # 0x601088 <stdout@@GLIBC_2.2.5>
   0x00000000004009f1 <+198>:	mov    %rax,%rdi
   0x00000000004009f4 <+201>:	call   0x400760 <fflush@plt>
   0x00000000004009f9 <+206>:	mov    -0x10(%rbp),%eax
   0x00000000004009fc <+209>:	cmp    %eax,-0xc(%rbp)
   0x00000000004009ff <+212>:	jne    0x400a14 <main+233>
   0x0000000000400a01 <+214>:	lea    0x1e0(%rip),%rdi        # 0x400be8
--Type <RET> for more, q to quit, c to continue without paging--
   0x0000000000400a08 <+221>:	call   0x4006e0 <puts@plt>
   0x0000000000400a0d <+226>:	call   0x400877 <giveFlag>
   0x0000000000400a12 <+231>:	jmp    0x400a20 <main+245>
   0x0000000000400a14 <+233>:	lea    0x1fd(%rip),%rdi        # 0x400c18
   0x0000000000400a1b <+240>:	call   0x4006e0 <puts@plt>
   0x0000000000400a20 <+245>:	mov    0x200661(%rip),%rax        # 0x601088 <stdout@@GLIBC_2.2.5>
   0x0000000000400a27 <+252>:	mov    %rax,%rdi
   0x0000000000400a2a <+255>:	call   0x400760 <fflush@plt>
   0x0000000000400a2f <+260>:	mov    $0x0,%eax
   0x0000000000400a34 <+265>:	mov    -0x8(%rbp),%rdx
   0x0000000000400a38 <+269>:	xor    %fs:0x28,%rdx
   0x0000000000400a41 <+278>:	je     0x400a48 <main+285>
   0x0000000000400a43 <+280>:	call   0x400700 <__stack_chk_fail@plt>
   0x0000000000400a48 <+285>:	leave
   0x0000000000400a49 <+286>:	ret
End of assembler dump.
(gdb) br 0x0000000000400962
Function "0x0000000000400962" not defined.
Make breakpoint pending on future shared library load? (y or [n]) n
(gdb) br *0x0000000000400962
Breakpoint 2 at 0x400962
(gdb) continue
Continuing.

Breakpoint 2, 0x0000000000400962 in main ()
(gdb) print $eax
$1 = 1705434425
(gdb) continue
Continuing.
Welcome to the number guessing game!
I'm thinking of a number. Can you guess it?
Guess right and you get a flag!
Enter your number: 1705434425
Your guess was 1705434425.
Looking for 1705434425.
You won. Guess was right! Here's your flag:
Flag file not found!  Contact an H3 admin for assistance.
[Inferior 1 (process 821905) exited normally]
(gdb) 
```

We first set a breakpoint until after the number is generated, move to that breakpoint, then read the number from the registers.

The reason we are reading from `%eax` is because function return values are placed in these registers. So when we finish executing the RNG function, its return value is placed in this register. We can also use the `%rax` register here. 64-bit numbers are placed in `%rax` and 32-bit numbers in `%eax`. In actuality, these are at the same location, but `%eax` only reads the lower 32 bits.

## Flag:

```
No flag for this one
```

## Concepts learnt:

- Assembly registers and how they work
- Debugging, accessing register vars while debugging and more
