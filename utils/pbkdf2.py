from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

def generate_key_from_password(password: str, salt: bytes = None):
    if salt is None:
        salt = get_random_bytes(16)

    key = PBKDF2(password, salt, dkLen=32, count=100000)

    return key, salt


def encode_salt(salt: bytes):
    return base64.b64encode(salt).decode()


def decode_salt(salt_str: str):
    return base64.b64decode(salt_str)