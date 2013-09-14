# Python imports
import requests

# Local imports
import exceptions
from timeline import Timeline
from contacts import Contacts

class User(object):
    """
    Represent an user for an application

    Access Google Glass timeline using : user.timeline
    Each user is defined by unique token : user.token
    """

    def __init__(self, app=None, token=None, refresh_token=None, tokens=None):

        if tokens:
            token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]

        self.app = app
        self.token = token
        self.refresh_token = refresh_token
        
        self.session = self.app.oauth.get_session(token=self.token)
        self.session.headers.update({'Content-Type': 'application/json'})

        self.timeline = Timeline(self)
        self.contacts = Contacts(self)

    def refresh_token(self):
        """
        Refresh user token and return tokens dict
        """
        if not self.refresh_token:
            raise Exception("No refresh token for this user")
        tokens = self.app.oauth.get_raw_access_token(data={
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }).json()
        self.token = tokens["access_token"]
        return self.tokens

    def request(self, *args, **kwargs):
        """
        Return a request with the user session
        """
        r = self.session.request(*args, **kwargs)
        try:
            r.raise_for_status()
        except requests.HTTPError, e:
            if e.response.status_code == 401:
                raise exceptions.RefreshTokenException()
            else:
                raise e
        return r

    @property
    def tokens(self):
        """
        Return tokens in a dict
        """
        return {
            "access_token": self.token,
            "refresh_token": self.refresh_token
        }

    def profile(self):
        """
        Return profile informations about this user
        """
        r = self.request("GET", "oauth2/v1/userinfo", params={'alt': 'json'})
        profile = r.json()
        
        if (profile is None
        or not "given_name" in profile
        or not "email" in profile
        or not "name" in profile):
            raise exceptions.UserException("Invalid user profile")
        return profile

    def location(self, lid="latest"):
        """
        Return the last known location or a specific location

        :param lid: location id ("latest" for the last known location)
        """
        r = self.request("GET", "mirror/v1/locations/%s" % (lid))
        location = r.json()
        
        if (location is None
        or not "latitude" in location
        or not "longitude" in location):
            raise exceptions.UserException("Invalid user location")
        return location
