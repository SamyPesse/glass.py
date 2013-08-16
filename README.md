glass.py
========

A simple library for building and testing Google Glass applications in Python using Mirror API.

## Examples :

#### hello.py

A simple helloworld which display a message when the user connect the application to his Glasses.

	import glass

	app = glass.Application(
		client_id="",
		client_secret="")

	@app.login
	def login(user):
		print "user : %s" % user.token
		user.timeline.post({
			"text": "Hello World!"
		})

	if __name__ == '__main__':
	    app.run()
