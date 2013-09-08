# Python imports
from flask import request, session, render_template, redirect, url_for

# Import glass library
import glass

# Import foursquare library
import foursquare

# Config imports
import config

app = glass.Application(
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    scopes=config.GOOGLE_SCOPES,
    template_folder="templates",
    static_url_path='/static',
    static_folder='static')

# Set the secret key for flask session.  keep this really secret: (but here it's not ;) )
app.web.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# map of userGoogleToken -> userFoursquareToken
FOURSQUARE_TOKENS = {}

# Return basic foursquare client
def foursquare_client():
    return foursquare.Foursquare(client_id=config.FOURSQUARE_CLIENT_ID, client_secret=config.FOURSQUARE_CLIENT_SECRET, redirect_uri=config.FOURSQUARE_CLIENT_REDIRECT)

@app.web.route("/")
def index():
    return render_template("index.html", auth=False)

@app.subscriptions.login
def login(user):
    print "google user: %s" % (user.token)
    session['token'] = user.token
    return redirect("/foursquare/authorize")

@app.subscriptions.location
def change_location(user):
    # Get last known location
    location = user.location()
    llat = location.get('latitude')
    llong = location.get('longitude')

    # Get foursquare client
    client = foursquare.Foursquare(access_token=FOURSQUARE_TOKENS[user.token])

    # Search venues on Foursquare
    venues = client.venues.search(params={'ll': llat+','+llong, 'llAcc': location.get('accuracy')})
    if len(venues['venues']) > 0:
    	# Post card with result
    	user.timeline.post_template("venue.html", venue=venues['venues'][0], llat=llat, llong=llong)


@app.web.route("/foursquare/authorize")
def foursquare_authorize():
    client = foursquare_client()
    return redirect(client.oauth.auth_url())

@app.web.route("/foursquare/callback")
def foursquare_callback():
    code = request.args.get('code', None)
    client = foursquare_client()

    if code is None or not 'token' in session:
        return render_template("index.html", auth=False)

    # Interrogate foursquare's servers to get the user's access_token
    access_token = client.oauth.get_token(code)

    # Add token to the map
    FOURSQUARE_TOKENS[session['token']] = access_token

    # Apply the returned access token to the client
    client.set_access_token(access_token)

    # Get the user's data
    user = client.users()
    username = user['user']['firstName']

    print "foursquare user: %s" % (access_token), username

    # Send a welcome message to the glass
    userglass = glass.User(app=app, token=session['token'])
    userglass.timeline.post(text="Welcome %s!" % username)
    
    return render_template("index.html", auth=True)


if __name__ == '__main__':
    print "Starting application at %s:%i" % (config.HOST, config.PORT)
    app.run(port=config.PORT, host=config.HOST)
    