from timeline import Timeline

class User(object):
    """
    Represent an user for an application
    """

    def __init__(self, app=None, token=None):
        self.app = app
        self.token = token
        self.session = self.app.oauth.get_session(token=self.token)
        self.timeline = Timeline(self)

    def profile(self):
        """
        Return profile informations about this user
        """
        profile = self.session.get("userinfo", params={'alt': 'json'}).json()
        if (profile is None
        or not "given_name" in profile
        or not "email" in profile
        or not "name" in profile):
            raise Exception("Invalid user profile")
        return profile