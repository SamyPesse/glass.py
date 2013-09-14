
class GlassException(RuntimeError):
    """Base excpetion for glass"""
    pass

class RefreshTokenException(GlassException):
    """user need a new access_token."""

class UserException(GlassException):
    """error with user data."""

class SubscriptionException(GlassException):
    """error posting user subscription."""

class ContactException(GlassException):
    """error with user contacts."""

class TimelineException(GlassException):
    """error with user timeline."""
