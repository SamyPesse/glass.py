# Import glass library
import glass

# Import app configs
import configs

app = glass.Application(
    name="Hello",
    client_id=configs.CLIENT_ID,
    client_secret=configs.CLIENT_SECRET,
    template_folder="templates"
)

@app.subscriptions.login
def login(user):
    print "user : %s" % user.token
    profile = user.profile()
    user.timeline.post_template("hello.html", name=profile.get("given_name"))

if __name__ == '__main__':
    app.run(port=8080)
    