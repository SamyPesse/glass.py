glass.py
========

A simple library for building and testing Google Glass applications in Python using Mirror API.

## Features :

* Post cards to timelines
* Get notification from subscriptions
* Emulator for testing the application


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
	user.timeline.post({
		"text": "Hello World!"
	})

if __name__ == '__main__':
    app.run(port=5000)
```

Enable the emulator (which will run at localhost:5000/emulator), emulator user can be identified by his token : "emulator"

```python
app.emulator = True
app.run(port=5000)
```

#### Insert Cards in timeline

Post html cards

```python
user.timeline.post({
	html: "Hello <b>World</b>"
})
```

Post html templates, templates are processed using Jinja2 template engine.

```python
user.timeline.post_template("message.html", {
	author: "Aaron",
	content: "Hey, How are you ?"
})
```

#### Subscribe to actions

Subscribe to an action "REPLY" :

```python
@app.action("REPLY")
def reply(user):
	print "User %s reply" % user.token
	user.timeline.post({
		"text": "Thank you!"
	})
```


