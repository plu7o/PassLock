import datetime

class Account:
	def __init__(self, service, name, email, password, url, id=None, date_added=None):
		self.service = service
		self.name = name
		self.email = email
		self.password = password
		self.url = url
		self.id = id if id is not None else None
		self.date_added = date_added if date_added is not None else datetime.datetime.now().isoformat()
	
	def __repr__(self) -> str:
		return f"(service:{self.service}, name:{self.name}, email:{self.email}, password:{self.password}, url:{self.url}, id:{self.id}, date:{self.date_added})"

	
