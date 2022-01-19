import sqlite3
from typing import List
import datetime
from model import Account
import secrets
import string
import os
from dotenv import load_dotenv

load_dotenv()
conn = sqlite3.connect(os.environ.get('secretPath'))
c = conn.cursor()

def create_table():
	c.execute("""CREATE TABLE IF NOT EXISTS passlock ( 
		service blob,
		name blob,
		email blob,
		password blob,
		url blob,
		id integer,
		date_added text
		)""")

create_table()

def get_all_accounts() -> List[Account]:
	with conn:	
		c.execute('select * from passlock')
		results = c.fetchall()
		accounts = []
		for result in results:
			accounts.append(Account(*result))
		return accounts

def get_account_by_service(service) -> List[Account]:
	with conn:
		c.execute('SELECT * FROM passlock WHERE service=:service', {'service': service})
		results = c.fetchall()
		accounts = []
		for result in results:
			accounts.append(Account(*result))
		return accounts

def get_account_by_email(email) -> List[Account]:
	with conn:
		c.execute('SELECT * FROM passlock WHERE email=:email', {'email': email})
		results = c.fetchall()
		accounts = []
		for result in results:
			accounts.append(Account(*result))
		return accounts

def get_account_by_name(name) -> List[Account]:
	with conn:
		c.execute('SELECT * FROM passlock WHERE name=:name', {'name': name})
		results = c.fetchall()
		accounts = []
		for result in results:
			accounts.append(Account(*result))
		return accounts

def gen_id():
	digits = string.digits
	id = ''.join(secrets.choice(digits) for i in range(5))
	return int(id)


def insert_account(account: Account):
	c.execute('select id from passlock')
	ids = c.fetchall()
	ID = gen_id()
	while ID in ids:
		ID == gen_id()
	account.id = ID

	with conn:
		c.execute('INSERT INTO passlock VALUES (:service, :name, :email, :password, :url, :id, :date_added)', 
		{'service': account.service,
		  'name': account.name,
		  'email': account.email, 
		  'password': account.password, 
		  'url': account.url, 
		  'id': account.id,
		  'date_added': account.date_added
		  })

def delete_account(id):
	c.execute('select count(*) from passlock')
	with conn:
		c.execute('DELETE from passlock WHERE id=:id', {'id': id})

def update_account(id: int, service: str, name: str, email: str, password: str, url: str):
	with conn:
		if service is not None and name is not None and email is not None and password is not None and url is not None:
			c.execute('UPDATE passlock SET service=:service, name=:name, email=:email, password=:password, url=:url WHERE id=:id', 
			{'id': id, 'service': service, 'name': name, 'email': email, 'password': password, 'url': url})
		elif service is not None:
			c.execute('UPDATE passlock SET service=:service WHERE id=:id', 
			{'id': id, 'service': service})
		elif name is not None:
			c.execute('UPDATE passlock SET name=:name WHERE id=:id', 
			{'id': id, 'name': name})
		elif email is not None:
			c.execute('UPDATE passlock SET email=:email WHERE id=:id', 
			{'id': id, 'email': email})
		elif password is not None:
			c.execute('UPDATE passlock SET password=:password WHERE id=:id', 
			{'id': id, 'password': password})
		elif url is not None:
			c.execute('UPDATE passlock SET url=:url WHERE id=:id', 
			{'id': id, 'url': url})
		
		

