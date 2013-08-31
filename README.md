glass.py
========

[![Code Now](https://friendco.de/widgets/image/codenow?url=https%3A%2F%2Fgithub.com%2FSamyPesse%2Fglass.py.git)](https://friendco.de/widgets/url/codenow?url=https%3A%2F%2Fgithub.com%2FSamyPesse%2Fglass.py.git)

A simple but powerful library for building and testing Google Glass applications in Python using Mirror API.

Glass.py uses Flask, Requests and Rauth.

I started this project for testing development of applications for Glass using Mirror API, but I'm not part of Explorer Program, so this library will soon contain an emulator.


## Features

* Post cards to timelines
* Get notification from subscriptions
* [Coming soon] Emulator for testing the application
* Built on [Requests](https://github.com/kennethreitz/requests) (v1.x)
* Built on [Flask](http://flask.pocoo.org/)

## Installation

Clone this repository :

	git clone https://github.com/SamyPesse/glass.py.git

Install dependencies :

	pip install -r requirements.txt

Install the library (maybe need to be sudo) :

	pip install .

## Test an Hello World with the emulator

	python examples/hello.py

## Example Usage

Full examples available at [master/examples](https://github.com/SamyPesse/glass.py/tree/master/examples).

#### Get started

A simple helloworld which display a message when the user connect the application to his Glasses.

```python
import glass

app = glass.Application(
	name="hello",
	client_id="",
	client_secret="")

@app.subscriptions.login
def login(user):
	print "user : %s" % user.token
	user.timeline.post(text="Hello World!")

if __name__ == '__main__':
    app.run(port=8080)
```

#### oAuth

Google Glass mirror API uses oAuth for authorizing an application to connect to the glasses. Go to the [Google APIs console](https://code.google.com/apis/console/) and create a new API project. Enable the Google Mirror API for your new project. The API is only available to developers who have Glass as part of the Explorer Program, so if it's not available for you, just pass this step.
Specify *http://localhost:8080/glass/oauth/callback* as callback url.

For authorizing the application to connect to your glasses, access the page : http://localhost:8080/glass/oauth/authorize
If you don't have Glass as part of the Explorer Program, use the emulator.

#### Emulator

Enable the emulator (which will run at localhost:8080/emulator/index.html), emulator user can be identified by his token : "emulator".
Emulator is not working yet and it's based on https://github.com/Scarygami/mirror-api

```python
app.emulator = True
app.run(port=8080)
```

#### Insert Cards in timeline

Post text cards :

```python
user.timeline.post(text="Hello World!")
```

Post HTML cards :

```python
user.timeline.post(html="Hello <b>World</b>")
```

Post HTML templates, templates are processed using Jinja2 template engine.
For templates you can use the full power of Jinja2 templates. Head over to the official [Jinja2 Template Documentation](http://jinja.pocoo.org/2/documentation/templates) for more information.

```python
user.timeline.post_template("message.html", author="Aaron", content="Hey, How are you ?")
```

Define the directory for the templates using :

```python
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
```

#### Subscribe to actions

Subscribe to an action "REPLY" :

```python
@app.subscriptions.action("REPLY")
def reply(user):
	print "User %s reply" % user.token
	user.timeline.post(text="Thank you!")
```

A new location is available for the current user, At this time, location notifications are sent every 10 minutes :

```python
@app.subscriptions.location
def change_location(user):
	print "User %s change location" % user.token
	user.timeline.post(text="You move !")
```

Access the user last known location using :

```python
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
```

#### Get user informations

Get profile data using :

```python
profile = user.profile()
print "Hello %s" % (profile.get("given_name"))
```

Get last known user location :

```python
location = user.location()
print "User is at (Lat: %s, Long: %s) (Accuracy: %s meters)" % (
		location.get('latitude'),
		location.get('longitude'),
		location.get('accuracy')
	)
```

#### Accessing the Flask web server

You can access the flask applciation for adding views (like index, about pages, ...) using :

```python
@app.web.route("/")
def index():
	return "Welcome on my Glass Application website !"
```
