# Standard Python libraries.
import os
import re
import cgi
import sys
import hashlib

# The Flask web application framework.
import flask

# Libraries for handling Google OAuth (i.e. user sign-in on the front page) authentication flow.
import google.oauth2.id_token
import google.auth.transport.requests

app = flask.Flask(__name__)

# Google client ID, taken from the Google API console - this value is inserted at build time.
clientID = "<<GOOGLECLIENTID>>.apps.googleusercontent.com"
clientSecret = "<<GOOGLECLIENTSECRET>>"

def getFile(theFilename):
    fileDataHandle = open(theFilename, encoding="latin-1")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

def putFile(theFilename, theData):
    fileDataHandle = open(theFilename, "w", encoding="latin-1")
    fileDataHandle.write(fileData)
    fileDataHandle.close()

def runCommand(theCommand):
    commandHandle = os.popen(theCommand)
    result = commandHandle.read()
    commandHandle.close()
    return(result)

@app.route("/")
def api():
    return "Hello world!"

# The Flask web server only deals with "/api/..." URLs. Redirect the Flask web server's index page (i.e. "/api/") to the main web server to serve the
# staticlly-generated API HTML documentation - from there we can include graphics and so on if wanted.
#@app.route("/")
#def api():
#    return flask.redirect("/api.html", code=302)

# Verify that a Google ID token is valid by checking it via Google's verification endpoint.
def verifyGoogleIDToken(theIDToken):
    try:
        # The IDInfo dict should always have the following keys set:
        # iss, sub, azp, aud, iat, exp
        # And, if the user is from a Google Domain:
        # hd
        # See for further details: https://developers.google.com/identity/sign-in/web/backend-auth#calling-the-tokeninfo-endpoint
        IDInfo = google.oauth2.id_token.verify_oauth2_token(theIDToken, google.auth.transport.requests.Request(), clientID)
        
        # If the issuer isn't Google, there's a problem.
        if IDInfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Wrong issuer.")
            
        # The aud value should match the client ID.
        if not IDInfo["aud"] == clientID:
            raise ValueError("Mismatched client ID.")
                
        # If the user is a member of a Google Domain (i.e. a school or business user) then record the domain, or the default
        # value of "-".
        googleHd = "-"
        if "hd" in IDInfo.keys():
            googleHd = IDInfo["hd"]
    except ValueError as e:
        # Invalid token.
        return "Error - " + repr(e)
    
    # At this point, we've verified the Google login token.
    return(IDInfo)

@app.route("/googleTokenSignin", methods=["POST"])
def googleTokenSignin():
    """
    Verify that a ID Token given by a client device is valid. This is for authentication of user logins to the site.
    """
    # Do the verification - if a string is returned, that's an error, but otherwise
    # we should have the user's information, including their email address.
    IDInfo = verifyGoogleIDToken(flask.request.values.get('idToken', None))
    if not isinstance(IDInfo, str):
        # Code goes here - check if the user is a valid user, not just any random passer-by with a GSuite account.
        if IDInfo["email"] in ["d.hicks@knightsbridgeschool.com", "k.milani@knightsbridgeschool.com", "s.harrison@knightsbridgeschool.com"]:
            # Code goes here - reset user's password (to long key) and return it.
            return "OK: " + IDInfo["email"] + " <<REMOTEPASSWORD>>"
        else:
            return "ERROR: Not a valid user on this system - " + IDInfo["email"]
    return IDInfo

if __name__ == "__main__":
    app.run()
