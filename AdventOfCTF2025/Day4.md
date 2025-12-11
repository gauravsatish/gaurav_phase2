#### Reverse Engineering

# Solution:
Pretty simple XOR, with the target bytes being hardcoded into the binary. We can just XOR them with the same number to get the flag.
Decompiled code:
```c
undefined8 FUN_00101362(long param_1)

{
  long counter;
  
  counter = 0;
  do {
    if (((int)*(char *)(param_1 + counter) ^ 0x42U) != (uint)(byte)(&DAT_00102110)[counter]) {
      return 0;
    }
    counter = counter + 1;
  } while (counter != 0x17);
  return 1;
}
```

solve script:
```python
target_bytes = [0x21, 0x31, 0x26, 0x39, 0x73, 0x2c, 0x36, 0x72, 0x1d, 0x36, 0x2a, 0x71,
                0x1d, 0x2f, 0x76, 0x73, 0x2c, 0x24, 0x30, 0x76, 0x2f, 0x71, 0x3f]

input = []
for byte in target_bytes:
    print(chr(byte ^ 0x42), end="")
```

# Flag:
```
csd{1nt0_th3_m41nfr4m3}
```