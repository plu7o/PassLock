import typer
from rich.console import Console
from rich.table import Table
import getpass
import string
import secrets
from passlib.hash import bcrypt
from model import Account
from database import get_account_by_service, get_account_by_email, get_account_by_name, get_all_accounts, insert_account
from passlock_crypt import gen_password, encrypt, decrypt

SECRET_KEY = 'kObYejRkQTRDAxAcVKPzi_ZeT93yHB7Riv9xKEC8lgk='
HASH = "$2b$14$dTRtdItLbtMenHUc.tuPxukJi3wW.ku86PLBWPLZb8CjncmtCS5fy"
app = typer.Typer()
console = Console()
hasher = bcrypt.using(rounds=14)

def verify_master(key=SECRET_KEY):
	master_password = getpass.getpass()
	passwd = f'{SECRET_KEY}{master_password}'
	if hasher.verify(passwd, HASH):
		console.print("[purple3]PASS🔒LOCK[/purple3]$ [blink green]Welcome Master[/blink green]")
		return True
	else:
		console.print("[purple3]PASS🔒LOCK[/purple3]$ [blink red]FUCK YOU!🖕[/blink red]")
		return exit(1)
		
@app.command(short_help='Utility function to generate random 48-long Token')
def gen_token(length: int=48):
	alphabet = string.ascii_letters + string.digits #+ string.punctuation
	token = ''.join(secrets.choice(alphabet) for i in range(length))
	console.print(f"[purple3]PASS🔒LOCK[/purple3]$ TOKEN: {token}")


@app.command(short_help='Utility Hash function using bcrypt hash')	
def get_hash(password: str):
	typer.echo('Generating hash...')
	console.print("[purple3]PASS🔒LOCK[/purple3]$ Generating Hash...")
	hashed_password = hasher.hash(password)
	typer.echo(f'HASH: {hashed_password}')
	console.print(f"[purple3]PASS🔒LOCK[/purple3]$ HASH: {hashed_password}")
	return hashed_password


@app.command(short_help='Adds Account to Database')
def add(service: str, email: str, name: str='', password: str='', url: str='', genpass: bool=True):
	if verify_master():
		if genpass:
			console.print(f"[purple3]PASS🔒LOCK[/purple3]$ Generating secure password...")
			password = gen_password(email, service)
		else:
			password = console.input("[purple3]PASS🔒LOCK[/purple3]$ Enter [bold cyan]password[/bold cyan] : ")
		console.print(f"[purple3]PASS🔒LOCK[/purple3]$ adding account to database: {service}|{email}:{password}")
		account = Account(service, name, email, encrypt(password), url)
		insert_account(account)
		console.print(f"[purple3]PASS🔒LOCK[/purple3]$ DONE ✅")

@app.command(short_help='Delete Account in Database')
def del():
	pass

@app.command(short_help='Update Account details')
def update():
	pass

@app.command(short_help='Find Account details by Service name')
def find(all: bool=False, email: bool=False, name: bool=False):
	if verify_master():
		if all:
			accounts = get_all_accounts()
		elif email:
			search = console.input("[purple3]PASS🔒LOCK[/purple3]$ Find by [bold cyan]Email[/bold cyan]? : ")
			accounts = get_account_by_email(search)
		elif name:
			search = console.input("[purple3]PASS🔒LOCK[/purple3]$ Find by [bold cyan]Name[/bold cyan]? : ")
			accounts = get_account_by_name(search)
		else:
			search = console.input("[purple3]PASS🔒LOCK[/purple3]$ Find by [bold cyan]Service[/bold cyan]? : ")
			accounts = get_account_by_service(search)
		
		table  = Table(show_header=True, header_style="bold blue", caption="Search Result")
		table.add_column("Service")
		table.add_column("Name")
		table.add_column("Email / Username")
		table.add_column("Password", min_width=20)
		table.add_column("URL")
		for account in accounts:
			table.add_row(account.service, account.name, account.email, decrypt(account.password), account.url)
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
