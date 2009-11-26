import urllib2

def register_basic_auth(credentials):
    """
    Takes an iterable of tuples in the form of (realm, uri, username, password)
    uri can be either a single URI, or a sequence of URIs.
    realm, user and password must be strings.
    This causes (user, passwd) to be used as authentication tokens when
    authentication for realm and a super-URI of any of the given URIs is given.
    """
    auth_handler = urllib2.HTTPBasicAuthHandler()
    for realm, uri, username, password in credentials:
        auth_handler.add_password(realm, uri, username, password)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
