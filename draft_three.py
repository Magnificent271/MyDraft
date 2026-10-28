import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_message(key: bytes, plaintext: str, aad: bytes = b"") -> bytes:
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode('utf-8'), aad)
    print(f'Зашифрованное сообщение: {nonce + ciphertext}')
    return nonce + ciphertext

def decrypt_message(key: bytes, encrypted: bytes, aad: bytes = b"") -> str:
    nonce = encrypted[:12]
    ciphertext = encrypted[12:]
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, aad)
    return plaintext.decode('utf-8')

def main():
    key = os.urandom(32)
    print(f'Ключ: {key}')
    secret = encrypt_message(key, "Секретное сообщение")
    print(decrypt_message(key, secret))

if __name__ == "__main__":
    main()
