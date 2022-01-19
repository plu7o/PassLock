from hashlib import sha256
from cryptography.fernet import Fernet
from passlib.hash import bcrypt
from os import urandom
import random
import string
import secrets

class Passlocker:
	def __init__(self, KEY):
		self.fernet = Fernet(KEY)
		self.hasher = bcrypt.using(rounds=14)
		self.ALPHABET = string.ascii_letters + string.digits + string.punctuation
	
	def encrypt(self, plaintext):
		return self.fernet.encrypt(plaintext.encode())

	def decrypt(self, cypher):
		return self.fernet.decrypt(cypher).decode()
		
	def gen_password(self, length):
			if not isinstance(length, int) or length < 8:
				raise ValueError("temp password must have positive length")

			chars = self.ALPHABET
			return "".join(chars[c % len(chars)] for c in urandom(length))
	
	def gen_token(self, length):
		alphabet = string.ascii_letters + string.digits #+ string.punctuation
		token = ''.join(secrets.choice(alphabet) for i in range(length))
		return token

	def get_hash(self, password):
		hashed_password = self.hasher.hash(password)
		return hashed_password
