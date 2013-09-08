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
    profile = user.profile()
    print "user : %s" % profile.get("given_name")
    user.timeline.post(text="Hello %s!" % profile.get("given_name"))

if __name__ == '__main__':
    app.run(port=8080)
    