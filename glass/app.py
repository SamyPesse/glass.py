from flask import Flask

class Application(object):

	def __init__(self, 
				client_id=None,
				client_secret=None):
		self.server = Flask()


	def login(self, rule, **options):
        """
      	A decorator that is used to register a function for when an user login
        """
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def run(self):
    	"""
    	Start the application
    	"""
    	self.server.run()
