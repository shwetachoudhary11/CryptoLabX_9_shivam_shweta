
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16


def pkcs7_pad(data):
    n = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([n]) * n


def encrypt_message(plaintext, key=None, iv=None):
    key = key or get_random_bytes(BLOCK_SIZE)
    iv = iv or get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pkcs7_pad(plaintext))

    return key, iv, ciphertext


def create_padding_oracle(key):
    def padding_oracle(iv, ciphertext):
        if len(iv) != BLOCK_SIZE:
            return False

        if not ciphertext or len(ciphertext) % BLOCK_SIZE:
            return False

        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = cipher.decrypt(ciphertext)
            n = plaintext[-1]

            return (
                1 <= n <= BLOCK_SIZE
                and plaintext.endswith(bytes([n]) * n)
            )
        except (ValueError, IndexError):
            return False

    return padding_oracle
