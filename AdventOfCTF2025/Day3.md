#### Miscellaneous

# Solution:
Checking `_dmarc.krampus.csd.lol`
```
id: 48618
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;_dmarc.krampus.csd.lol.	IN TXT
**;; ANSWER SECTION:
_dmarc.krampus.csd.lol.	300 IN TXT "v=DMARC1; p=reject; rua=mailto:dmarc@krampus.csd.lol; ruf=mailto:forensics@ops.krampus.csd.lol; fo=1; adkim=s; aspf=s"**
```
This reveals the `ops.krampus.csd.lol` domain:
```
id: 5822
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;ops.krampus.csd.lol.	IN TXT
**;; ANSWER SECTION:
ops.krampus.csd.lol.	300 IN TXT "internal-services: _ldap._tcp.krampus.csd.lol _kerberos._tcp.krampus.csd.lol _metrics._tcp.krampus.csd.lol"**
```
This now gives us three new SRV record names. Checking the records of these give us:
`_ldap._tcp.krampus.csd.lol`:
```
id: 31211
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;_ldap._tcp.krampus.csd.lol. IN SRV
**;; ANSWER SECTION:
_ldap._tcp.krampus.csd.lol. 300	IN SRV 0 0 389 dc01.krampus.csd.lol.**
```
`_kerberos._tcp.krampus.csd.lol`:
```
id: 991
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;_kerberos._tcp.krampus.csd.lol.	IN SRV
**;; ANSWER SECTION:
_kerberos._tcp.krampus.csd.lol.	300 IN SRV 0 0 88 dc01.krampus.csd.lol.**
```
`_metrics._tcp.krampus.csd.lol`:
```
id: 63675
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;_metrics._tcp.krampus.csd.lol. IN SRV
**;; ANSWER SECTION:
_metrics._tcp.krampus.csd.lol. 300 IN SRV 0 0 443 beacon.krampus.csd.lol.**
```

These give us two new subdomains: `dc01.krampus.csd.lol` and `beacon.krampus.csd.lol`. The former yields nothing useful, but the latter reveals the following:
```
id: 56802
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;beacon.krampus.csd.lol.	IN TXT
**;; ANSWER SECTION:
beacon.krampus.csd.lol.	300 IN TXT "config=ZXhmaWwua3JhbXB1cy5jc2QubG9s=="**
```
`config=ZXhmaWwua3JhbXB1cy5jc2QubG9s==` looks like it contains a base64 string, so decoding it gives us the domain `exfil.krampus.csd.lol`.

Looking up the records for this:
```
id: 30619
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;exfil.krampus.csd.lol.	IN TXT
**;; ANSWER SECTION:
exfil.krampus.csd.lol.	300 IN TXT "status=active; auth=dkim; selector=syndicate"**
```
This tells us that the DKIM selector is `syndicate`. Looking up `syndicate._domainkey.krampus.csd.lol`:
```
id: 5058
opcode: QUERY
status: NOERROR
flags: QR RD RA CD
;; QUESTION SECTION:
;syndicate._domainkey.krampus.csd.lol. IN TXT
**;; ANSWER SECTION:
syndicate._domainkey.krampus.csd.lol. 300 IN TXT "v=DKIM1; k=rsa; p=Y3Nke2RuNV9tMTlIVF9CM19LMU5ENF9XME5LeX0="**
```

This contains another base64 string, which upon decoding gives the flag:

# Flag:
```
csd{dn5_m19HT_B3_K1ND4_W0NKy}
```

TODO:
Include more expanation on how DNS works. Will update once I learn more about this.