# Libs imports
import flask
import rauth
import json
import os

# Local imports
from user import User
from subscriptions import Subscriptions

class Application(object):
    OAUTH_ACCESS_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
    OAUTH_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
    OAUTH_REDIRECT_URI = "authentification/google"
    OAUTH_API_BASE_URL = "https://www.googleapis.com/"
    OAUTH_SCOPES = [
        'https://www.googleapis.com/auth/glass.location',
        'https://www.googleapis.com/auth/glass.timeline',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'
    ]

    def __init__(self, 
                name="",
                client_id=None,
                client_secret=None,
                emulator=False,
                debug=True,
                template_folder='templates'):
        self.name = name
        self.emulator = emulator
        self.debug = debug
        self.web = flask.Flask(self.name,
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'emulator'),
            static_url_path='/emulator')
        self.template_folder = template_folder
        self.logger = self.web.logger
        self.subscriptions = Subscriptions(app=self)
        self.oauth = rauth.OAuth2Service(name=self.name,
                                  client_id=client_id,
                                  client_secret=client_secret,
                                  access_token_url=self.OAUTH_ACCESS_TOKEN_URL,
                                  authorize_url=self.OAUTH_AUTHORIZE_URL,
                                  base_url=self.OAUTH_API_BASE_URL)

    @property
    def oauth_redirect_uri(self):
        return "%s/glass/oauth/callback" % (self.host)

    def _oauth_authorize(self):
        """
        (view) Display the authorization window for Google Glass
        """
        params = {
            'approval_prompt': 'force',
            'scope': " ".join(self.OAUTH_SCOPES),
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

        # Add subscriptions
        self.subscriptions.init_user(user)

        # Call endpoint for user login
        self.subscriptions.call_endpoint("login", user)

        return token

    def run(self, host="http://localhost", port=8080, debug=None):
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

        # Run webserver
        self.web.run(port=self.port)


