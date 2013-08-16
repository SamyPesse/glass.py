from timeline import Timeline

class User(object):
	"""
	Represent an user for an application
	"""

	def __init__(self, app, token):
		self.app = app
		self.token = token
		self.timeline = Timeline(self)