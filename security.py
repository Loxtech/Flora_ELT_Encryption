import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

KEY_FILE = "secret.key"

def get_or_create_key() -> bytes:
    """Henter eksisterende krypteringsnøgle eller genererer en ny."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as kf:
            kf.write(key)
    else:
        with open(KEY_FILE, "rb") as kf:
            key = kf.read()
    return key


# ==============================================================================
# VALG AF KRYPTERINGSMETODE OG BEGRUNDELSE
# ==============================================================================
"""
Fernet / AES-128-CBC med HMAC-SHA256.

BEGRUNDELSE FOR VALG FREM FOR DE ANDRE METODER:
1. Fernet vs. Rå AES-CBC (Metode 2):
   Rå AES-CBC kræver manuel håndtering af PKCS7-padding og styring af IV (Initialization Vector).
   Vigtigst af alt mangler rå CBC indbygget autentificering (integritetskontrol). Dette gør 
   data sårbar overfor 'padding oracle'-angreb og datamanipulation. Fernet anvender HMAC-SHA256
   ovenpå AES-CBC, hvilket garanterer både fortrolighed og dataintegritet.

2. Fernet vs. AES-GCM (Metode 1):
   AES-GCM er en fremragende AEAD-tilstand, men kræver at man selv opbevarer og styrer
   nonce (12 bytes), autentificerings-tag (16 bytes) og ciphertext separat for hver enkelt celle.
   Fernet pakker automatisk IV, ciphertext og HMAC-tag sammen i én Base64-kodet streng.
   Dette gør det ideelt til tabeldata (CSV og MySQL VARCHAR/TEXT-kolonner), da hele den
   krypterede værdi kan gemmes som en simpel tekststreng i én enkelt kolonne uden at ændre databasestrukturen.
"""
# ==============================================================================


# --- METODE 1: AES-GCM ---
def encrypt_aes_gcm(data: str, raw_key_32bytes: bytes) -> tuple:
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(raw_key_32bytes), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return ciphertext, nonce, encryptor.tag

# --- METODE 2: AES-CBC (Rå med PKCS7 padding) ---
def encrypt_aes_cbc(data: str, raw_key_16bytes: bytes) -> tuple:
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(raw_key_16bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext, iv

# --- METODE 3: AES-CBC med Fernet (VALGT LØSNING) ---
def encrypt_val(val: str, key: bytes) -> str:
    """Krypterer en enkelt streng/værdi med Fernet og returnerer Base64-tekst."""
    if val is None:
        return None
    f = Fernet(key)
    return f.encrypt(str(val).encode('utf-8')).decode('utf-8')

def decrypt_val(cipher_text: str, key: bytes) -> str:
    """Dekrypterer en Fernet Base64-tekst tilbage til oprindelig streng."""
    if cipher_text is None:
        return None
    f = Fernet(key)
    return f.decrypt(str(cipher_text).encode('utf-8')).decode('utf-8')