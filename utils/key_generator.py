import os
import base64
import secrets
import string


def generate_aes_key(length=16):
    return os.urandom(length)


def generate_secure_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_base64_key(length=32):
    return base64.b64encode(os.urandom(length)).decode()