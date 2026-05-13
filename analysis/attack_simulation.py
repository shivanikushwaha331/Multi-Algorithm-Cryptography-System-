import itertools

def brute_force_demo(ciphertext):
    chars = "abc123"
    for guess in itertools.product(chars, repeat=3):
        attempt = ''.join(guess)
        if attempt == ciphertext:
            return f"Cracked: {attempt}"
    return "Not cracked"
