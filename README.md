### Author:
* plu7o

---
### Discription: 


This is Educational Project
Terminal CLI Password-Manager with encrypted password storage and Master password secured 
I wanted to create a simple password storage system that is somewhat secure, also to learn about hashing and encryption and methods to securly store passwords

!!! USE ONLY AT OWN RISK !!!
i'm not responsible for any harm that may be caused by yourself or others

---
### Libaries:
#### CLI
* Typer
* rich
#### Encryption & Security
* cryptography
* passlib
* python-dotenv
* getpass
* secrets
#### DB
* sqlite3

---
### Todo:
- [x] Implement Add command
- [x] Implement Find command
- [x] Implement Delete command
- [x] Implement Update command
- [x] Loading Secret-keys securly (.env file)
- [x] Encrypt all db entries
- [x] Add ID unique identifyer to account model
- [x] rebuild passlocker.py to class
- [x] Make strong password generator
- [x] Relocate passlock.db
- [x] Add requirments.txt
- [x] Add short - flags to CLI
- [ ] more...?

---
### Installation:
    $ git clone https://github.com/plu7o/PassLock.git
    $ pip install -r requirments.txt

---
### Usage:
    $ python3 passlock.py COMMAND [OPTIONS] [ARGS]
    $ python3 passlock.py --help
    	
    >	Commands:
    	add        Adds Account to Database
    	delete     Delete Account in Database
    	find       Find Account details by Identifier
    	gen-token  Utility function to generate random 48-long Token
    	get-hash   Utility Hashing function to Hash password using bcrypt
    	update     Update Account details
---
### Example:
#### Adding account: 
    $ python3 passlock.py add [service] [email] [OPTIONS]
    $ python3 passlock.py add google test@gamil.com -u https://google.com

#### Deleting account:
    $ python3 passlock.py delete [ID]
    $ python3 passlock.py delete 38950

#### Updating account:
    $ python3 passlock.py update [ID] [OPTIONS]
    $ python3 passlock.py update 38950 --email newemail@gmail.com

#### Find account:
    $ python3 passlock.py find | [OPTIONS]
    $ python3 passlock.py find | find -s google

---
### Refrences:
* https://www.realpythonproject.com/3-ways-to-store-and-read-credentials-locally-in-python/
* https://martinheinz.dev/blog/59
* https://charlesleifer.com/blog/creating-a-personal-password-manager/
* https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_quick_guide.htm
* https://sqreen.github.io/DevelopersSecurityBestPractices/safe-password-storage/python
* https://typer.tiangolo.com/tutorial/
* https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
* https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
* https://cloud.google.com/kms/docs/envelope-encryption
* https://www.realpythonproject.com/3-ways-to-store-and-read-credentials-locally-in-python/
* https://docs.python.org/3/library/secrets.html
