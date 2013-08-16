# Libs imports
import flask
import rauth
import json

# Local imports
from user import User

class Application(object):
    OAUTH_ACCESS_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
    OAUTH_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
    OAUTH_REDIRECT_URI = "authentification/google"
    OAUTH_API_BASE_URL = "https://www.googleapis.com/oauth2/v1/"
    OAUTH_SCOPES = (
        'https://www.googleapis.com/auth/userinfo.profile '
        'https://www.googleapis.com/auth/userinfo.email '
    )

    def __init__(self, 
                name="",
                client_id=None,
                client_secret=None,
                emulator=False,
                debug=True):
        self.name = name
        self.emulator = emulator
        self.debug = debug
        self.web = flask.Flask(self.name)
        self.logger = self.web.logger
        self.endpoints = {}
        self.oauth = rauth.OAuth2Service(name=self.name,
                                  client_id=client_id,
                                  client_secret=client_secret,
                                  access_token_url=self.OAUTH_ACCESS_TOKEN_URL,
                                  authorize_url=self.OAUTH_AUTHORIZE_URL,
                                  base_url=self.OAUTH_API_BASE_URL)


    def add_endpoint(self, endpoint, callback):
        """
        Add a function to an endpoint

        :param endpoint: the endpoint name (ex: "login")
        :param callback: the endpoint callback to add 
        """
        if not endpoint in self.endpoints:
            self.endpoints[endpoint] = []
        self.logger.debug("Add callback to endpoint %s" % endpoint)
        self.endpoints[endpoint].append(callback)

    def call_endpoint(self, endpoint, *args, **kwargs):
        """
        Call callbacks for and endpoint

        :param endpoint: the endpoint name (ex: "login")
        :param *args, **kwargs: params for the callback
        """
        if not endpoint in self.endpoints:
            self.endpoints[endpoint] = []
        self.logger.debug("Call endpoint %s" % endpoint)
        for callback in self.endpoints[endpoint]:
            callback(*args, **kwargs)

    def login(self, f):
        """
        A decorator that is used to register a function for when an user login
        """
        self.add_endpoint("login", f)
        return f

    @property
    def oauth_redirect_uri(self):
        return "http://%s/glass/oauth/callback" % (self.host)

    def _oauth_authorize(self):
        """
        (view) Display the authorization window for Google Glass
        """
        params = {
            'approval_prompt': 'force',
            'scope': self.OAUTH_SCOPES,
            'state': '/profile',
            'redirect_uri': self.oauth_redirect_uri,
            'response_type': 'code'
        }
        url = self.oauth.get_authorize_url(**params)
        return flask.redirect(url)

    def _oauth_callback(self):
        """
        (view) Callback for the oauth
        """
        token = self.oauth.get_access_token(data={
            'code': flask.request.args.get('code', ''),
            'redirect_uri': self.oauth_redirect_uri,
            'grant_type': 'authorization_code'
        }, decoder=json.loads)
        user = User(token=token, app=self)
        self.call_endpoint("login", user)
        return token

    def run(self, host="localhost", port=8080, debug=None):
        """
        Start the application server
        """
        if self.emulator:
            pass

        self.port = port
        self.host = host
        if port != 80:
            self.host = "%s:%i" % (self.host, self.port)

        # OAUTH
        self.web.add_url_rule('/glass/oauth/authorize', 'oauth_authorize', self._oauth_authorize)
        self.web.add_url_rule('/glass/oauth/callback', 'oauth_callback', self._oauth_callback)

        self.web.debug = debug or self.debug
        self.web.run(port=self.port)


