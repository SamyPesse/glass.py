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

@app.subscriptions.location
def change_location(user):
    # Get last known location
    location = user.location()

    # Post card with location infos
    user.timeline.post(text="You move to (Lat: %s, Long: %s) (Accuracy: %s meters)" % (
        location.get('latitude'),
        location.get('longitude'),
        location.get('accuracy')
    ))

if __name__ == '__main__':
    app.run(port=8080)
    