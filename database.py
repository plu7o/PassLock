import sqlite3
from typing import List
import datetime
from model import Account

conn = sqlite3.connect('/usr/share/.passlock/passlock.db')
c = conn.cursor()

def create_table():
	c.execute("""CREATE TABLE IF NOT EXISTS passlock ( 
		service text,
		name text,
		email text,
		password blob,
		url text,
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

def insert_account(account: Account):
	c.execute('select count(*) from passlock')
	with conn:
		c.execute('INSERT INTO passlock VALUES (:service, :name, :email, :password, :url, :date_added)', {'service': account.service, 'name': account.name, 'email': account.email, 'password': account.password, 'url': account.url, 'date_added': account.date_added})
