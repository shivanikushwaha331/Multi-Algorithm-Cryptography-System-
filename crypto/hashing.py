import hashlib
from utils.history import save_history

def hash_data(data, algorithm="sha256"):
    if algorithm == "md5":
        result = hashlib.md5(data.encode()).hexdigest()
    elif algorithm == "sha1":
        result = hashlib.sha1(data.encode()).hexdigest()
    elif algorithm == "sha256":
        result = hashlib.sha256(data.encode()).hexdigest()
    elif algorithm == "sha512":
        result = hashlib.sha512(data.encode()).hexdigest()

    save_history("Hash", algorithm.upper())

    return result