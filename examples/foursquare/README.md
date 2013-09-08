Complete Example: Unofficial Foursquare App for Google Glass
========

This example is a very simple foursquare application for Google Glass (unofficial, I'm not related to Foursquare). The goal is to display, whenever the user location change, a card with the best place around him and action to check in it.
The code is only 100 lines but for the moment it only display the best place around him (no check in action).

## How to run it ?

Open the file config.py and change the different Client IDs and Secret Ids for Google APIs and Foursquare API.
Install the foursquare python library and glass.py :

    pip install foursquare
    pip install git+ssh://git@github.com/SamyPesse/glass.py.git@master#egg=glass.py

Run the application :

    python app.py

## Screens

The homepage of the application :
[![Screen](https://raw.github.com/SamyPesse/glass.py/master/examples/foursquare/screens/web.png)](https://raw.github.com/SamyPesse/glass.py/master/examples/foursquare/screens/web.png)

The card in the Google Glass :
[![Screen](https://raw.github.com/SamyPesse/glass.py/master/examples/foursquare/screens/glass.png)](https://raw.github.com/SamyPesse/glass.py/master/examples/foursquare/screens/glass.png)

## Code Explained

First of all, we create a new Glass Application using glass.py :

```python
app = glass.Application(
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    scopes=config.GOOGLE_SCOPES,
    template_folder="templates",
    static_url_path='/static',
    static_folder='static')
app.web.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
```

We create a map to store the tokens for Foursquare users :

```python
# map of userGoogleToken -> userFoursquareToken
FOURSQUARE_TOKENS = {}
```

We define the homepage for our application website :

```python
@app.web.route("/")
def index():
    return render_template("index.html", auth=False)
```

And the callback when the user is logged with Google

```python
@app.subscriptions.login
def login(user):
    print "google user: %s" % (user.token)
    session['token'] = user.token
    return redirect("/foursquare/authorize")
```

Authentification for Google is done, we now have to work with Foursquare authentification :

```python
def foursquare_client():
    return foursquare.Foursquare(client_id=config.FOURSQUARE_CLIENT_ID,
    client_secret=config.FOURSQUARE_CLIENT_SECRET,
    redirect_uri=config.FOURSQUARE_CLIENT_REDIRECT)


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
```

When the user is logged with Google Glass and Foursquare, we can now handle location change :

```python
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
```

And finally start the application, glass.py will manage the rest for us :

```python
if __name__ == '__main__':
    print "Starting application at %s:%i" % (config.HOST, config.PORT)
    app.run(port=config.PORT, host=config.HOST)
```
