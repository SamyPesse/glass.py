# Local imports
from timeline import Timeline

class User(object):
    """
    Represent an user for an application

    Access Google Glass timeline using : user.timeline
    Each user is defined by unique token : user.token
    """

    def __init__(self, app=None, token=None):
        self.app = app
        self.token = token
        self.session = self.app.oauth.get_session(token=self.token)
        self.session.headers.update({'Content-Type': 'application/json'})
        self.timeline = Timeline(self)

    @property
    def emulator(self):
        return self.token == "emulator"

    def profile(self):
        """
        Return profile informations about this user
        """
        profile = self.session.get("oauth2/v1/userinfo", params={'alt': 'json'}).json()
        
        if (profile is None
        or not "given_name" in profile
        or not "email" in profile
        or not "name" in profile):
            raise Exception("Invalid user profile")
        return profile

    def location(self, lid="latest"):
        """
        Return the last known location or a specific location

        :param lid: location id ("latest" for the last known location)
        """
        location = self.session.get("mirror/v1/locations/%s" % (lid)).json()
        
        if (location is None
        or not "latitude" in location
        or not "longitude" in location):
            raise Exception("Invalid user location")
        return location