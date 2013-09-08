# Application
HOST = "localhost"
PORT = 5000

# Google
GOOGLE_CLIENT_ID = "1052883900395.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "rfYSj8_Y9XevHUbFAFfK-Q5y"
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/glass.location',
    'https://www.googleapis.com/auth/glass.timeline',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

# Foursquare
FOURSQUARE_CLIENT_ID = "QG0XUORRDRH1H4S0R2XITZTLYLGPV30F13OYAXAZE20Y5DEX"
FOURSQUARE_CLIENT_SECRET = "B34IC0NTD3GNW2LT3VW2GCWZRLFVFPO1DRC1MAR2WUN1FXPR"
FOURSQUARE_CLIENT_REDIRECT = "http://%s:%i/foursquare/callback" % (HOST, PORT)
