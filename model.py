import datetime

class Account:
	def __init__(self, service, name, email, password, url, date_added=None):
		self.service = service
		self.name = name
		self.email = email
		self.password = password
		self.url = url
		self.date_added = date_added if date_added is not None else datetime.datetime.now().isoformat()
	
	def __repr__(self) -> str:
		return f"({self.service}, {self.name}, {self.email}, {self.password}, {self.url}, {self.date_added})"	
