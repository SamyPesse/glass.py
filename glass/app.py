from flask import Flask

class Application(object):

	def __init__(self, 
				name="",
				client_id=None,
				client_secret=None):
		self.name = name
		self.server = Flask()


	def login(self, rule, **options):
        """
      	A decorator that is used to register a function for when an user login
        """
        def decorator(f):
            return f
        return decorator

    def run(self):
    	"""
    	Start the application
    	"""
    	self.server.run()
