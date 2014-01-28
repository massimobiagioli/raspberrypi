from itertools import cycle, izip
import base64


def xor_encrypt(message, key):
    """
    Effettua criptaggio XOR
    @param message: messaggio da criptare
    @param key: chiave per il criptaggio
    @return: messaggio criptato
    """
    return base64.b64encode(''.join(chr(ord(c)^ord(k)) for c,k in izip(message, cycle(key))))

def xor_decrypt(cyphered, key):
    """
    Effettua decriptaggio XOR
    @param cyphered: messaggio criptato
    @param key: chiave per il decriptaggio
    @return: messaggio decriptato
    """
    return ''.join(chr(ord(c)^ord(k)) for c,k in izip(base64.b64decode(cyphered), cycle(key)))


### MAIN ############################################
if __name__ == '__main__':
    m = xor_encrypt("Un1t&", "Qwerty456$%&")
    print xor_decrypt(m, "Qwerty456$%&")