import streamlit as st
import base64
import time
import itertools
import pandas as pd
import matplotlib.pyplot as plt

# Crypto imports
from crypto.aes import encrypt_aes, decrypt_aes, encrypt_file, decrypt_file
from crypto.rsa import generate_keys, encrypt_rsa, decrypt_rsa
from crypto.classical import caesar_encrypt, caesar_decrypt, vigenere_encrypt, vigenere_decrypt
from crypto.hashing import hash_data
from utils.key_generator import generate_aes_key
from analysis.security_analysis import analyze_algorithm


# ---------------- UI STYLE ---------------- #
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1518770660439-4636190af475");
            background-size: cover;
        }
        .block-container {
            background-color: rgba(0, 0, 0, 0.6);
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Multi Cryptography System", layout="wide")
set_background()

st.title("🔐 Multi Cryptography System")
st.markdown("### Secure • Analyze • Encrypt • Learn")
st.divider()

# ---------------- SIDEBAR ---------------- #
option = st.sidebar.selectbox("Select Module", [
    "Encryption/Decryption",
    "Hashing",
    "Hybrid Encryption 🔐",
    "File Encryption 📁",
    "Performance Benchmark 📊",
    "Attack Simulation ⚔️",
    "Security Analysis",
    "History "
])


# ---------------- ENCRYPTION ---------------- #
if option == "Encryption/Decryption":

    algo = st.selectbox("Algorithm", ["AES", "RSA", "Caesar", "Vigenere"])
    text = st.text_area("Enter Text")

    if algo == "AES":
        key = generate_aes_key()

        if st.button("Encrypt"):
            enc = encrypt_aes(text, key)
            st.session_state["aes"] = (enc, key)
            st.success("Encrypted successfully")
            st.write(enc)

        if st.button("Decrypt"):
            if "aes" in st.session_state:
                enc, key = st.session_state["aes"]
                st.success("Decrypted text:")
                st.write(decrypt_aes(enc, key))

    elif algo == "RSA":
        pub, priv = generate_keys()

        if st.button("Encrypt"):
            enc = encrypt_rsa(text, pub)
            st.session_state["rsa"] = (enc, priv)
            st.write("Encrypted:", enc)

        if st.button("Decrypt"):
            if "rsa" in st.session_state:
                enc, priv = st.session_state["rsa"]
                st.write("Decrypted:", decrypt_rsa(enc, priv))

    elif algo == "Caesar":
        shift = st.slider("Shift", 1, 25)
        st.write("Encrypted:", caesar_encrypt(text, shift))
        st.write("Decrypted:", caesar_decrypt(text, shift))

    elif algo == "Vigenere":
        key = st.text_input("Key")
        st.write("Encrypted:", vigenere_encrypt(text, key))
        st.write("Decrypted:", vigenere_decrypt(text, key))


# ---------------- HASHING ---------------- #
elif option == "Hashing":

    text = st.text_area("Enter Text")
    algo = st.selectbox("Algorithm", ["md5", "sha1", "sha256", "sha512"])

    if st.button("Generate Hash"):
        st.write("Hash:", hash_data(text, algo))


# ---------------- HYBRID ---------------- #
elif option == "Hybrid Encryption 🔐":

    st.subheader("RSA + AES Hybrid Encryption")
    text = st.text_area("Enter Text")

    if st.button("Encrypt"):
        pub, priv = generate_keys()
        aes_key = generate_aes_key()

        enc_data = encrypt_aes(text, aes_key)
        enc_key = encrypt_rsa(base64.b64encode(aes_key).decode(), pub)

        st.session_state["hybrid"] = (enc_data, enc_key, priv)

        st.success("Encryption Successful")
        st.write("Encrypted Data:", enc_data)
        st.write("Encrypted AES Key:", enc_key)

    if st.button("Decrypt"):
        if "hybrid" in st.session_state:
            enc_data, enc_key, priv = st.session_state["hybrid"]

            aes_key = base64.b64decode(decrypt_rsa(enc_key, priv))
            decrypted = decrypt_aes(enc_data, aes_key)

            st.success("Decrypted Text:")
            st.write(decrypted)


# ---------------- FILE ENCRYPTION (FIXED) ---------------- #
elif option == "File Encryption 📁":

    st.subheader("🔐 File Encryption (Password-Based)")

    mode = st.radio("Choose Mode", ["Encrypt File", "Decrypt File"])

    from crypto.aes import encrypt_file, decrypt_file
    from utils.pbkdf2 import generate_key_from_password, encode_salt, decode_salt

    # -------- ENCRYPT -------- #
    if mode == "Encrypt File":

        file = st.file_uploader("Upload File")
        password = st.text_input("Enter Password", type="password")

        if file and password:
            file_bytes = file.read()
            filename = file.name

            if st.button("Encrypt"):
                key, salt = generate_key_from_password(password)

                encrypted = encrypt_file(file_bytes, key, filename)

                st.success("File Encrypted")

                st.write("🔑 Save this Salt (Base64):")
                st.code(encode_salt(salt))

                st.download_button(
                    "Download Encrypted File",
                    encrypted,
                    file_name=filename + ".enc"
                )

    # -------- DECRYPT -------- #
    elif mode == "Decrypt File":

        file = st.file_uploader("Upload Encrypted File")
        password = st.text_input("Enter Password", type="password")
        salt_input = st.text_input("Enter Salt")

        if file and password and salt_input:
            encrypted_bytes = file.read()

            try:
                salt = decode_salt(salt_input)
                key, _ = generate_key_from_password(password, salt)

                if st.button("Decrypt"):
                    decrypted, filename = decrypt_file(encrypted_bytes, key)

                    st.success("Decryption Successful")

                    st.download_button(
                        "Download File",
                        decrypted,
                        file_name=filename
                    )

            except:
                st.error("Wrong password or salt")







# ---------------- BENCHMARK ---------------- #
elif option == "Performance Benchmark 📊":

    st.subheader("Encryption Speed Comparison")

    text = "Benchmark Test Data"

    key = generate_aes_key()
    start = time.time()
    encrypt_aes(text, key)
    aes_time = time.time() - start

    pub, _ = generate_keys()
    start = time.time()
    encrypt_rsa(text, pub)
    rsa_time = time.time() - start

    df = pd.DataFrame({
        "Algorithm": ["AES", "RSA"],
        "Time (seconds)": [aes_time, rsa_time]
    })

    fig, ax = plt.subplots()
    ax.bar(df["Algorithm"], df["Time (seconds)"])
    ax.set_title("Performance Comparison")
    ax.set_ylabel("Time (seconds)")

    st.pyplot(fig)


# ---------------- ATTACK SIMULATION ---------------- #
elif option == "Attack Simulation ⚔️":

    st.subheader("Brute Force Simulation (Advanced)")

    target = st.text_input("Enter Password (max 8 characters)")
    max_attempts = st.slider("Max Attempts (simulation limit)", 1000, 100000, 10000)

    if st.button("Start Attack"):

        if not target:
            st.warning("Enter a password first")
        elif len(target) > 8:
            st.error("Password too long (max 8)")
        else:
            import string

            chars = string.ascii_lowercase + string.digits  # a-z + 0-9
            attempts = 0
            start = time.time()

            found = False

            for length in range(1, len(target) + 1):
                for guess in itertools.product(chars, repeat=length):
                    attempt = ''.join(guess)
                    attempts += 1

                    # Stop if found
                    if attempt == target:
                        st.success(f"Password Cracked: {attempt}")
                        found = True
                        break

                    # Stop if limit reached
                    if attempts >= max_attempts:
                        st.warning("Stopped early (limit reached)")
                        break

                if found or attempts >= max_attempts:
                    break

            end = time.time()

            st.write(f"Attempts tried: {attempts}")
            st.write(f"Time Taken: {end - start:.2f} seconds")

            if not found:
                st.info("Password not cracked (increase limit for deeper simulation)")


# ---------------- SECURITY ANALYSIS ---------------- #
elif option == "Security Analysis":

    algo = st.selectbox("Algorithm", ["AES", "RSA", "DES", "MD5", "SHA-256"])
    result = analyze_algorithm(algo)

    if isinstance(result, dict):
        st.json(result)
    else:
        st.write(result)

# --------------------history ----------------- #
elif option == "History 📜":

    from utils.history import load_history
    import pandas as pd

    st.subheader("📜 Activity History")

    history = load_history()

    if history:
        df = pd.DataFrame(history)

        # Format table
        df = df[["time", "action", "algorithm"]]

        st.dataframe(df, use_container_width=True)

        # Download option
        csv = df.to_csv(index=False).encode()
        st.download_button("Download History CSV", csv, "history.csv")

        # Clear history button
        if st.button("Clear History"):
            with open("data/history.json", "w") as f:
                f.write("[]")
            st.success("History Cleared")
            st.rerun()

    else:
        st.info("No history available yet")