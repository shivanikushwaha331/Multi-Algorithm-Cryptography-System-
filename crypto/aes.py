from Crypto.Cipher import AES
import base64
from utils.history import save_history



# ---------------- TEXT ENCRYPTION ---------------- #
def encrypt_aes(plaintext: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    save_history("Encrypt", "AES")
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()


def decrypt_aes(ciphertext: str, key: bytes) -> str:
    data = base64.b64decode(ciphertext)

    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    save_history("Decrypt", "AES")
    return decrypted.decode()


# ---------------- FILE ENCRYPTION (WITH FILENAME) ---------------- #
def encrypt_file(file_bytes: bytes, key: bytes, filename: str) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_bytes)

    # Store filename length + filename
    filename_bytes = filename.encode()
    filename_len = len(filename_bytes).to_bytes(2, 'big')
    save_history("Encrypt", "AES")
    return filename_len + filename_bytes + cipher.nonce + tag + ciphertext


def decrypt_file(encrypted_bytes: bytes, key: bytes):
    # Extract filename
    filename_len = int.from_bytes(encrypted_bytes[:2], 'big')
    filename = encrypted_bytes[2:2 + filename_len].decode()

    start = 2 + filename_len
    nonce = encrypted_bytes[start:start + 16]
    tag = encrypted_bytes[start + 16:start + 32]
    ciphertext = encrypted_bytes[start + 32:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    save_history("Decrypt", "AES")
    return decrypted, filename