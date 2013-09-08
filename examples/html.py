# Import glass library
import glass

# Import app configs
import configs

app = glass.Application(
    name="Hello",
    client_id=configs.CLIENT_ID,
    client_secret=configs.CLIENT_SECRET
)

@app.subscriptions.login
def login(user):
    print "user : %s" % user.token
    user.timeline.post(html="Hello <b>World</b>")

if __name__ == '__main__':
    app.run(port=8080)
    