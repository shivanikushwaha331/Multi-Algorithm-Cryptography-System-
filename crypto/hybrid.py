from crypto.aes import encrypt_aes
from crypto.rsa import encrypt_rsa

def hybrid_encrypt(data, public_key, aes_key):
    encrypted_data = encrypt_aes(data, aes_key)
    encrypted_key = encrypt_rsa(aes_key.decode(), public_key)
    return encrypted_data, encrypted_key