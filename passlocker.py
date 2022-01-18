from hashlib import sha256
import random
from cryptography.fernet import Fernet
import string

key = "Bg3KAwPUyOzp1LZKWFmP-rcz6PcufwLM52GFmHZ_SAc="
fernet = Fernet(key)
ALPHABET = string.ascii_letters + string.digits + string.punctuation

def build_password(plain, service):
	salt = get_hexdigest(key, service)[:20]
	hash = get_hexdigest(salt, plain)
	return ''.join((salt, hash))

def get_hexdigest(salt, plain):
	return sha256((f'{salt}{plain}').encode()).hexdigest()

def encrypt(plaintext):
	return fernet.encrypt(plaintext.encode())

def decrypt(cypher):
	return fernet.decrypt(cypher).decode()
	
def gen_password(plaintext, service, length=18, alphabet=ALPHABET):
    raw_hexdigest = build_password(plaintext, service)

    # Convert the hexdigest into decimal
    num = int(raw_hexdigest, 16)

    # What base will we convert `num` into?
    num_chars = len(alphabet)

    # Build up the new password one "digit" at a time,
    # up to a certain length
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(alphabet[idx])

    return ''.join(chars)
