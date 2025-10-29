# 1. Custom Encryption

> Can you get sense of this code file and write the function that will decode the given encrypted file content. Find the encrypted file here [flag_info](https://artifacts.picoctf.net/c_titan/18/enc_flag) and [code file](https://artifacts.picoctf.net/c_titan/18/custom_encryption.py) might be good to analyze and get the flag.

## Solution:

Here is my decryption program:
```python
def generator(g, x, p):
    return pow(g, x) % p

cipher = [260307, 491691, 491691, 2487378, 2516301, 0, 1966764, 1879995, 1995687, 1214766, 0, 2400609, 607383, 144615, 1966764, 0, 636306, 2487378, 28923, 1793226, 694152, 780921, 173538, 173538, 491691, 173538, 751998, 1475073, 925536, 1417227, 751998, 202461, 347076, 491691]


text_key = "trudeau"


a = 94
b = 29
p = 97
g = 31

u = generator(g, a, p)
v = generator(g, b, p)
key = generator(v, a, p)
b_key = generator(u, b, p)
shared_key = key
print(f"""####################
u: {u}
v: {v}
key: {key}
b_key: {b_key}
shared_key: {shared_key}
###################\n\n""")

for i, num in enumerate(cipher):
    cipher[i] = chr(int(num / (311 * shared_key)))

plaintext = ""

for i, char in enumerate(cipher):
    key_char = text_key[i % len(text_key)]
    decrypted_char = chr(ord(char) ^ ord(key_char))
    plaintext += decrypted_char

print(plaintext[::-1])
```
Few points of interest here:
- The inverse of an xor operation is an xor operation.
- We start with the output cipher and try to inverse the operations starting from the last to the first.

## Flag:

```
picoCTF{custom_d2cr0pt6d_751a22dc}
```

## Notes:

- None

## Resources:

- None


***
