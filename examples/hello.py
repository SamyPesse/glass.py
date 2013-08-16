# Import glass library
import glass

# Import app configs
import configs

app = glass.Application(
	client_id=configs.CLIENT_ID,
	client_secret=configs.CLIENT_SECRET)

@app.login
def login(user):
	print "user : %s" % user.token
	user.timeline.post(text="Hello World!")

if __name__ == '__main__':
    app.run(port=8080)
	