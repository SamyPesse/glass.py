# Application
HOST = "localhost"
PORT = 5000

# Google
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/glass.location',
    'https://www.googleapis.com/auth/glass.timeline',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

# Foursquare
FOURSQUARE_CLIENT_ID = ""
FOURSQUARE_CLIENT_SECRET = ""
FOURSQUARE_CLIENT_REDIRECT = "http://%s:%i/foursquare/callback" % (HOST, PORT)
