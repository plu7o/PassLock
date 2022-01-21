import typer
from halo import Halo
from rich.console import Console
from rich.table import Table
from model import Account
from passlocker import Passlocker

passlocker = Passlocker()
from database import get_account_by_service, get_account_by_email, get_account_by_name, get_all_accounts, insert_account, delete_account, update_account

app = typer.Typer()
console = Console()

prefix = '[purple3]PASS🔒LOCK[/purple3]$'
		
@app.command(short_help='Utility function to generate random 48-long Token')
def gen_token(length: int=typer.Option(48, '-l', help='length of the generated token')):
	with Halo(text=f"Generating Token...", spinner='dots'):
		token = passlocker.gen_token(length)
	console.print(f"{prefix} TOKEN: {token}")

@app.command(short_help='Utility Hashing function to Hash password using bcrypt')	
def gen_hash(password: str):
	with Halo(text=f"Generating Hash...", spinner='dots'):
		hashed_password = passlocker.gen_hash(password)
	console.print(f"{prefix} HASH: {hashed_password}")

@app.command(short_help='Utility function to generate ')
def gen_password(length: int=typer.Option(12, '-l', help='length of the generated CSPRNG Password')):
	with Halo(text=f"Generating Password...", spinner='dots'):
		password = passlocker.gen_password(length)
	console.print(f"{prefix} Password: {password}")
	
@app.command(short_help='Adds Account to Database')
def add(service: str, email: str, \
	name: str=typer.Option('/', '-n', '--name', help='Add Name to account when creating entry', show_default=False), \
	url: str=typer.Option('/','-u', '--url', help='Add Url to account when creating entry', show_default=False), \
	gen: bool=typer.Option(True, '-g', '--no-gen', help='No password gets generated prompt to enter Existing Password', show_default=False)):
	
	if passlocker.verify_master():
		if gen:
			with Halo(text=f"Generating Password...", spinner='dots'):
				password = passlocker.gen_password(18)
		else:
			password = console.input(f"{prefix} Enter Account [bold cyan]password[/bold cyan] : ")
		console.print(f"{prefix} adding account to database: {service} | {email}:{password}")
		
		account = Account(passlocker.encrypt(service), \
		passlocker.encrypt(name), \
		passlocker.encrypt(email), \
		passlocker.encrypt(password), \
		passlocker.encrypt(url))
		
		insert_account(account)
		console.print(f"{prefix} DONE✅")

@app.command(short_help='Delete Account in Database')
def delete(id: int):
	if passlocker.verify_master():
		console.print(f"{prefix} DELETING Account: {id}")
		delete_account(id)
		console.print(f"{prefix} DONE✅")

@app.command(short_help='Update Account details')
def update(id: int, \
	service: str=typer.Option(None, '-s', '--service', help='Update Service'),\
	name: str=typer.Option(None, '-n', '--name', help='Update Name'), \
	email: str=typer.Option(None, '-e', '--email', help='Update emial'), \
	password: str=typer.Option(None, '-p', '--password', help='Update passsword'), \
	url: str=typer.Option(None, '-u', '--url', help='Update URL')):
	
	if passlocker.verify_master():
		service = passlocker.encrypt(service) if service is not None else service
		name = passlocker.encrypt(name) if name is not None else name
		email = passlocker.encrypt(email) if email is not None else email
		password = passlocker.encrypt(password) if password is not None else password
		url = passlocker.encrypt(url) if url is not None else url

		console.print(f"{prefix} UPDATING Account: {id}")
		update_account(id, service, name, email, password, url)
		console.print(f"{prefix} DONE✅")
	
@app.command(short_help='Find Account details by Identifier')
def find(service: bool=typer.Option(False, '-s', '--service', help='Search accounts by Service'), \
	name: bool=typer.Option(False, '-n', '--name', help='Search accounts by Name'), \
	email: bool=typer.Option(False, '-e', '--name', help='Search accounts by Email')):
	
	if passlocker.verify_master():
		if service:
			search = console.input(f"{prefix} Find by [bold cyan]Service[/bold cyan]? : ")
			accounts = get_account_by_service((search))
		elif email:
			search = console.input(f"{prefix} Find by [bold cyan]Email[/bold cyan]? : ")
			accounts = get_account_by_email(search)
		elif name:
			search = console.input(f"{prefix} Find by [bold cyan]Name[/bold cyan]? : ")
			accounts = get_account_by_name(search)
		else:
			accounts = get_all_accounts()
		
		table  = Table(show_header=True, header_style="bold blue", caption="Search Result")
		table.add_column("ID")
		table.add_column("Service")
		table.add_column("Name")
		table.add_column("Email / Username")
		table.add_column("Password", min_width=20)
		table.add_column("URL")
		
		for account in accounts:
			table.add_row(str(account.id), \
			passlocker.decrypt(account.service), \
			passlocker.decrypt(account.name), \
			passlocker.decrypt(account.email), \
			passlocker.decrypt(account.password), \
			passlocker.decrypt(account.url))
		
		console.print(table)

banner = """
                       [green3]=*%@@%#=[/green3]       
    		     [green3]:@@#-::-*@@:[/green3]     
 ____               [green3]:@@.       @@:[/green3] _               _    
|  _ \ __ _ ___ ___ [green3]:@@+#@@@@%+@@:[/green3]| |    ___   ___| | __
| |_) / _` / __/ __|[green3]@@@@@/  \@@@@@[/green3]| |   / _ \ / __| |/ /     
|  __/ (_| \__ \__ [green3]#@@@@@\__/@@@@@#[/green3] |__| (_) | (__|   <      
|_|   \__,_|___/___[green3]:@@@@@@:.@@@@@@:[/green3]_____\___/ \___|_|\_\       
                    [green3]:%@@@@@@@@@@%:[/green3]  
		      [green3]:+#@@@@#+:[/green3]     			 """


	
if __name__ == '__main__':
	console.print(banner, style='bold purple3')
	app()
