from rich.console import Console
from cryptography.fernet import Fernet
from passlib.hash import bcrypt
from dotenv import load_dotenv
import getpass
import os
import sys
import string
import secrets
import subprocess

class Passlocker:
	def __init__(self):
		self.hasher = bcrypt.using(rounds=14)
		self.ALPHABET = string.ascii_letters + string.digits + string.punctuation
		self.console = Console()
		self.prefix = '[purple3]PASS🔒LOCK[/purple3]$'
		if self.check_key():
			self.SECRET_KEY = self.load_key('secretKey')
			self.SECRET_USER = self.load_key('secretUser')
			self.fernet = Fernet(self.SECRET_KEY)
		else:
			self.gen_secret_key()
			self.SECRET_KEY = self.load_key('secretKey')
			self.SECRET_USER = self.load_key('secretUser')
			self.fernet = Fernet(self.SECRET_KEY)

	def gen_secret_key(self):
		self.console.print(f"{self.prefix} [blink red]NO SECRET KEY FOUND[/blink red]")
		self.console.print(f"{self.prefix} Enter [cyan]Master[/cyan] Password")
		master_password = getpass.getpass()
		self.console.print(f"{self.prefix} Generating Key...")
		secretKEY = Fernet.generate_key()
		secretKEY = secretKEY.decode('utf-8')
		self.console.print(f"{self.prefix} Generating Hash...")
		secretUSER = self.gen_hash(f'{secretKEY}{master_password}')
		self.console.print(f"{self.prefix} Setting up Database...")
		subprocess.run(['mkdir','/root/.passlock'])
		self.console.print(f"{self.prefix} Writing keys...")
		self.write_keys(secretKEY, secretUSER)
	
	def write_keys(self, secretKEY, secretUSER):
		keys = [f'secretKey="{secretKEY}"\n', f'secretUser="{secretUSER}"\n']
		with open(os.path.join(sys.path[0], '.env'), 'w', encoding='utf-8') as f:
			f.writelines(keys)	
			f.write('secretPath="/root/.passlock/passlock.db"')

	def load_key(self, key):
		load_dotenv()
		return os.environ.get(key)

	def check_key(self):
		if self.load_key('secretKey') is not None:
			return True
		else:
			return False

	def encrypt(self, plaintext):
		return self.fernet.encrypt(plaintext.encode())

	def decrypt(self, cypher):
		return self.fernet.decrypt(cypher).decode()
	
	def gen_password(self, length):
		chars = self.ALPHABET
		stage_1 =  "".join(chars[c % len(chars)] for c in os.urandom(length))
		stage_2 = self.gen_hash(stage_1)
		while True:
			password =  ''.join(secrets.choice(f'{stage_2}' + chars) for i in range(length)).replace(" ", "")
			if (any(c.islower() for c in password) and any(c.isupper() for c in password)
				and sum(c.isdigit() for c in password) >=3):
				break
		return password
		
	def gen_token(self, length):
		chars = string.ascii_letters + string.digits
		token = ''.join(secrets.choice(chars) for i in range(length))
		return token

	def gen_hash(self, input):
		hash = self.hasher.hash(input)
		return hash
	
	def verify_master(self):
		attempt = 0
		while attempt != 3:
			master_password = getpass.getpass()
			passwd = f'{self.SECRET_KEY}{master_password}'
			if self.hasher.verify(passwd, self.SECRET_USER):
				self.console.print(f"{self.prefix} [blink green]Welcome Master[/blink green]")
				attempt = 0
				return True
			else:
				self.console.print(f"{self.prefix} [blink red]FUCK YOU!🖕[/blink red]")
				self.console.print(f"{self.prefix} [blink green]Try again[/blink green]")
				attempt += 1




