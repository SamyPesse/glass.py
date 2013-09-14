# Python imports
import hashlib
import json
import flask
from uuid import uuid4

# Local imports
import exceptions
from user import User


class Subscriptions(object):
    """
    Subscriptions repressent subscriptions from the app to glasses notifications
    """

    def __init__(self, app):
        self.app = app
        self.subscriptions = {} # Map of subscriptions to send to google api
        self.endpoints = {}    # map of endpoint -> callback function
        self.tokens = {} # map of userToken -> tokens dict

    def add_subscription(self, collection, operations=[]):
        """
        Add a subscription for glasses

        :param collection: Collection to subscribe to (ex: "timeline")
        :param operations: (list or string) operation to subscribe to (ex: "UPDATE")
        """
        m = hashlib.md5()

        if isinstance(operations, basestring):
            operations = [operations]
        operations.sort()
        m.update("%s:%s" % (collection, "-".join(operations)))
        subscription_id = m.hexdigest()
        if subscription_id in self.subscriptions:
            return False

        # Add subscription to map
        self.subscriptions[subscription_id] = {
            "id": subscription_id,
            "collection": collection,
            "operations": operations
        }

        # Add view for subscription
        def handler():
            data = json.loads(request.data)
            userid = data["userToken"]
            if not userid in self.tokens:
                raise Exception("Callback for a non-existant user")
            user = User(app=self.app, tokens=self.tokens[userid])
            if data["collection"] == "timeline":
                for action in data["actions"]:
                    self.call_endpoint("action."+action["type"], user)
            elif data["collection"] == "locations":
                self.call_endpoint("location", user)

        self.app.web.add_url_rule('/glass/callback/%s' % subscription_id, 'callback_%s' % subscription_id, handler)


    def add_endpoint(self, endpoint, callback):
        """
        Add a function to an endpoint

        :param endpoint: the endpoint name (ex: "login")
        :param callback: the endpoint callback to add 
        """
        if not endpoint in self.endpoints:
            self.endpoints[endpoint] = []
        self.app.logger.debug("Add callback to endpoint %s" % endpoint)
        self.endpoints[endpoint].append(callback)

    def call_endpoint(self, endpoint, *args, **kwargs):
        """
        Call callbacks for and endpoint

        :param endpoint: the endpoint name (ex: "login")
        :param *args, **kwargs: params for the callback
        """
        back = None

        if not endpoint in self.endpoints:
            return back

        self.app.logger.debug("Call endpoint %s" % endpoint)
        for callback in self.endpoints[endpoint]:
            back = callback(*args, **kwargs)
        return back

    def init_user(self, user):
        """
        Connect to the user notifications using registred subscriptions
        """
        userUniqueId = [k for k, v in self.tokens.iteritems() if v == user.token]
        if len(userUniqueId) == 0:
            userUniqueId = str(uuid4())
            if userUniqueId in self.tokens:
                # random id alredy used
                return self.subscribe_user(user)

        # Set user token to the map
        self.tokens[userUniqueId] = user.tokens

        # Subscribe
        for sid, subscription in self.subscriptions.items():
            callback_url = "%s/glass/callback/%s" % (self.app.host, subscription["id"])
            result = user.request("POST", "/mirror/v1/subscriptions", data=json.dumps({
                "collection": subscription["collection"],
                "userToken": userUniqueId,
                "operation": subscription["operations"],
                "callbackUrl": callback_url
            })).json()
            if (result is None or not "id" in result):
                raise exceptions.SubscriptionException("Error posting subscription ", result)
        return True

    def login(self, f):
        """
        A decorator that is used to register a function for when an user login
        """
        self.add_endpoint("login", f)
        return f

    def location(self, f):
        """
        A decorator that is used to register a function for when an user location changed
        """
        self.add_subscription("locations")
        self.add_endpoint("location", f)
        return f

    def action(self, action, **options):
        """
        A decorator that is used to register a function for an user action
        """
        def decorator(f):
            self.add_subscription("timeline", "UPDATE")
            self.add_endpoint("action.%s" % action, f)
        return decorator
