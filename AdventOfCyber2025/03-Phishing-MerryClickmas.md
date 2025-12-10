# Solution:

Following all the instructions:
```console
~/Rooms/AoC2025/Day02# ./server.py 
Starting server on http://0.0.0.0:8000
10.48.158.217 - - [10/Dec/2025 12:36:01] "GET / HTTP/1.1" 200 -
[2025-12-10 12:36:01] Captured -> username: admin    password: unranked-wisdom-anthem    from: 10.48.158.217
10.48.158.217 - - [10/Dec/2025 12:36:01] "POST /submit HTTP/1.1" 303 -
10.48.158.217 - - [10/Dec/2025 12:36:01] "GET / HTTP/1.1" 200 -
10.48.158.217 - - [10/Dec/2025 12:39:02] "GET / HTTP/1.1" 200 -
```

Logging in as `factory` with password `unranked-wisdom-anthem`, we see an email with the subject:
`Urgent: Production & Shipping Request \u2014 1984000 Units (Next 2 Weeks`

# Flag:
```
unranked-wisdom-anthem
1984000
```
