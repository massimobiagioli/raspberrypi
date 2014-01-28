from itertools import cycle, izip
import base64


def xor_encrypt(message, key):
    return base64.b64encode(''.join(chr(ord(c)^ord(k)) for c,k in izip(message, cycle(key))))

def xor_decrypt(cyphered, key):
    return ''.join(chr(ord(c)^ord(k)) for c,k in izip(base64.b64decode(cyphered), cycle(key)))

if __name__ == '__main__':
    m = xor_encrypt("Un1t&", "Qwerty456$%&")
    print xor_decrypt(m, "Qwerty456$%&")