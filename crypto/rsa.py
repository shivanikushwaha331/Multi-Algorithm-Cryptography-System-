from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

from utils.history import save_history


def generate_keys():
    key = RSA.generate(2048)
    return key.publickey(), key

def encrypt_rsa(plaintext, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    save_history("Encrypt", "RSA")
    return base64.b64encode(cipher.encrypt(plaintext.encode())).decode()


def decrypt_rsa(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    save_history("Decrypt", "RSA")
    return cipher.decrypt(base64.b64decode(ciphertext)).decode()