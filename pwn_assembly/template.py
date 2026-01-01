from pwn import *

context.update(arch="amd64")
code = ""
while True:
    line = input()
    if line == "done":
        break
    code = code + line + "\n"
code = asm(code.strip())

p = process("/challenge/run")
p.send(code)

print(p.recvall().decode())
