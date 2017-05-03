# xorbreak

## Installation
Assuming you already have Python 2.7 (and pip) installed, run:
```
$ pip2.7 install docopt
$ git clone https://github.com/augusto-ludtke/xorbreak.git
```

## Usage
### Find the most probable key lengths
```
$ cd xorbreak
$ python xorbreak.py  -f examples/ciphertext_coursera.txt
Ciphertext: 470 bytes
Most probable key lengths
Length        Index of coincidence
  28              7.853
  14              6.997
  21              6.704
   7              5.467
  27              0.699
  30              0.654
  20              0.547
  26              0.499
  29              0.497
  18              0.470
```

### Guess the key value
```
$ python xorbreak.py -g -l 7 examples/ciphertext_coursera.txt
Ciphertext: 470 bytes
Probable key: ....S.> (BA1F91B253CD3E)
Cleartext: Cryptography is the practice and study of techniques for, among other things, secure communication in the presence of attackers. Cryptography has been used for hundreds, if not thousands, of years, but traditional cryptosystems were designed and evaluated in a fairly ad hoc manner. For example, the Vigenere encryption scheme was thought to be secure for decades after it was invented, but we now know, and this exercise demonstrates, that it can be broken very easily.
```

### Decrypt the ciphertext with a known key
```
$ python xorbreak.py -d -k BA1F91B253CD3E examples/ciphertext_coursera.txt
Ciphertext: 470 bytes
Key: ....S.> (BA1F91B253CD3E)
Cleartext: Cryptography is the practice and study of techniques for, among other things, secure communication in the presence of attackers. Cryptography has been used for hundreds, if not thousands, of years, but traditional cryptosystems were designed and evaluated in a fairly ad hoc manner. For example, the Vigenere encryption scheme was thought to be secure for decades after it was invented, but we now know, and this exercise demonstrates, that it can be broken very easily.
```

## What does Bruce Schneier say about simple-XOR?
> "The simple-XOR algorithm is really an embarassment; it's nothing more than a Vigenere polyalphabetic cipher...There's no real security here. This kind of encryption is trivial to break, even without computers...An XOR might keep your kid sister from reading your files, but it won't stop a cryptanalyst for more than a few minutes." (Applied Cryptography)