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

# 2. Mini RSA

> Let's decrypt this: [ciphertext](https://jupiter.challenges.picoctf.org/static/ee7e2388b45f521b285334abb5a63771/ciphertext)? Something seems a bit small.

## Solution:

Looking at the hint, I searched up what happens when the `e` value is too little. The encryption formula for RSA is `c = m^e mod n`. But when `e` is too little, `m^e` can sometimes be lesser than `n`, hence completely negating the `mod n` operation and making this cipher trivial to decrypt. All you have to do is find the `e`th root of the cipher.

Putting the cipher through an online full precision calculator:
`2205316413931134031074603746928247799030155221252519872649649212867614751848436763801274360463406171277838056821437115883619169702963504606017565783537203207707757768473109845162808575425972525116337319108047893250549462147185741761825125 ^(1÷3)`
= `13016382529449106065894479374027604750406953699090365388202874238148389207291005`

Converting this number into hex, we get:
`7069636F4354467B6E3333645F615F6C41726733725F655F36303663653030347D`

And finally, converting this hex to ASCII text:
`picoCTF{n33d_a_lArg3r_e_606ce004}`

All sites used are listed in the resources.

## Flag:

```
picoCTF{n33d_a_lArg3r_e_606ce004}
```

## Concepts learnt:

A critical vulnerability that arises when the value of e is too small

## Notes:

- Tried making a python script for this, but getting the full precision required was not possible without external libraries so I opted for using online full precision calculators

## Resources:

- [Full Precision Calculator](https://www.mathsisfun.com/calculator-precision.html)
- [Decimal to Hex](https://www.rapidtables.com/convert/number/decimal-to-hex.html)
- [Hex to ASCII Text](https://www.rapidtables.com/convert/number/hex-to-ascii.html)


***

# 3. RSA Oracle

> Can you abuse the oracle? An attacker was able to intercept communications between a bank and a fintech company. They managed to get the [message](https://artifacts.picoctf.net/c_titan/34/secret.enc) (ciphertext) and the [password](https://artifacts.picoctf.net/c_titan/34/password.enc) that was used to encrypt the message. After some intensive reconassainance they found out that the bank has an oracle that was used to encrypt the password and can be found here `nc titan.picoctf.net 62386`. Decrypt the password and use it to decrypt the message. The oracle can decrypt anything except the password.

# Solution

Looking at the hints, we know that we must employ a "Known Plaintext Attack". This is a form of exploit where you have some method of getting encrypted ciphertexts for any arbitrary input. In this challenge, we also get decryption capabilities for anything that isn't the password.
Therefore to solve this, we must use the mathematical properties of RSA encryption. The RSA encryption formula is:
`c = m^e mod n`, where e is the public exponent, and n is the modulus.

Suppose we have a pre-existing cipher `c1 = m^e mod n`. We can take any arbitrary integer (say 2), and encrypt it in the same fashion. Let us call this cipher `c2`.
If we multiply them together:
`c1*c2 = m^e mod n * 2^e mon n = (2m)^e mod n`, if we decrypt this new `c1*c2` cipher, we get the value of `2m`, and hence we can find the value of `m`.

I made a script to get the password:
```python
from pwn import remote

def encrypt(n, conn):
    conn.sendline(b"E")
    conn.recv(timeout=1)
    conn.sendline(n)
    conn.recvuntil(b"(m ^ e mod n) ")
    return int(conn.recvline(timeout=1).strip().decode())

def decrypt(c, conn):
    conn.sendline(b'D')
    conn.recv(timeout=1)
    conn.sendline(c)
    conn.recvuntil(b"(c ^ d mod n): ")
    return conn.recvline(timeout=1).strip().decode()

PORT = 62386
conn = remote('titan.picoctf.net', PORT)
conn.recv(timeout=1)

cipher = 873224563026311790736191809393138825971072101706285228102516279725246082824238887755080848591049817640245481028953722926586046994669540835757705139131212

two_cipher = encrypt(b'\x02', conn)
conn.recv(timeout=1)
multi_res = cipher*two_cipher
m2 = decrypt(str(multi_res), conn)

print(m2)
```

```console
[+] Opening connection to titan.picoctf.net on port 62386: Done
/home/gaurav/Projects/picogym/Cryptography/rsa_oracle/decrypt.py:13: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  conn.sendline(c)
7264c86a66
[*] Closed connection to titan.picoctf.net port 62386
```
This gives us the hex value of `2m`, and by dividing it by 2, we get `3932643533`. Converting this to ASCII text, we finally get the password `92d53`.

Now, using one of the hints given in the challenge, it is a trivial matter to decrypt the secret. We use the following command:
```console
$: openssl enc -aes-256-cbc -d -in secret.enc -k 92d53
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
picoCTF{su((3ss_(r@ck1ng_r3@_92d53250}
```

## Flag:
```
picoCTF{su((3ss_(r@ck1ng_r3@_92d53250}
```

## Concepts Learnt:
- The mathematical property of RSA that lets us exploit this
- Known plaintext attacks

## Notes
- This challenge was quite frustrating to me, because I spent like an hour doing the wrong encoding method for the netcat connection, ranging from converting the ascii value of the input to bytes, to giving the ascii value itself, to other random shit. Finally I realized my mistake and how it actually worked.