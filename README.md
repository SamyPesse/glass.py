glass.py
========

A simple library for building and testing Google Glass applications in Python using Mirror API.

## About this project


## Features

* Post cards to timelines
* Get notification from subscriptions
* Emulator for testing the application
* Built on [Requests](https://github.com/kennethreitz/requests) (v1.x)
* Built on [Flask](http://flask.pocoo.org/)

## Installation

Clone this repository :

	git clone https://github.com/SamyPesse/glass.py.git

Install dependencies :

	pip install -r requirements.txt

## Example Usage

#### Get started

A simple helloworld which display a message when the user connect the application to his Glasses.

```python
import glass

app = glass.Application(
	name="hello",
	client_id="",
	client_secret="")

@app.login
def login(user):
	print "user : %s" % user.token
	user.timeline.post(text="Hello World!")

if __name__ == '__main__':
    app.run(port=8080)
```

#### oAuth

Google Glass mirror API uses oAuth for authorizing an application to connect to the glasses.

1. Go to the [Google APIs console](https://code.google.com/apis/console/) and create a new API project.
2. Click Services and enable the Google Mirror API for your new project. The API is only available to developers who have Glass as part of the Explorer Program, so if it's not available for you, just pass this step.
3. Click **API Access** and create an OAuth 2.0 client ID for a web application.
4. Specify the product name and icon for your Application. These fields appear on the OAuth grant screen presented to your users.
5. Select **Web application** and specify any value for the hostname, such as localhost
6. Click **Edit settings**... for the client ID to specify redirect URIs. Specify **http://localhost:8080/glass/oauth/callback**
7. Make note of the client ID and secret from the Google APIs Console. You'll need it to configure your application.

For authorizing the application to connect to your glasses, access the page : **http://localhost:8080/glass/oauth/authorize**
If you don't have Glass as part of the Explorer Program, use the emulator.

#### Emulator

Enable the emulator (which will run at localhost:8080/emulator), emulator user can be identified by his token : "emulator"

```python
app.emulator = True
app.run(port=8080)
```

#### Insert Cards in timeline

Post HTML cards.

```python
user.timeline.post(html="Hello <b>World</b>")
```

Post HTML templates, templates are processed using Jinja2 template engine.

```python
user.timeline.post_template("message.html", author="Aaron", content="Hey, How are you ?")
```

#### Subscribe to actions

Subscribe to an action "REPLY" :

```python
@app.action("REPLY")
def reply(user):
	print "User %s reply" % user.token
	user.timeline.post(text="Thank you!")
```


