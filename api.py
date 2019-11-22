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
clientID = "<<GOOGLECLIENTID>>"
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
                
        # If the user is a member of a Google Domain (i.e. a school or business user) then record the domain, or the default value of "-".
        googleHd = "-"
        if "hd" in IDInfo.keys():
            googleHd = IDInfo["hd"]
    except ValueError as e:
        # Invalid token.
        return "Error - " + repr(e)
    
    # At this point, we've verified the Google login token.
    return(IDInfo)

# Check the parameters passed to an API call. Takes a dict of parameter names / values and a list of required parameter names.
# If a listed required parameter is not found, throws an error. Note that "idToken" is always considered a required parameter.
def checkParameters(theValues, requiredParameterNames):
    requiredParameters = {}
    # Verify the user's ID Token - if an error message (as a string) isn't returned, we know we have a valid
    # array with user data in it.
    IDInfo = verifyGoogleIDToken(theValues.get('idToken', None))
    if isinstance(userInfo, basestring):
        raise ValueError("Invalid idToken.")
    for requiredParameterName in requiredParameterNames:
        theValue = theValues.get(requiredParameterName, None)
        if theValue == None:
            raise ValueError("Parameter named " + requiredParameterName + " not found.")
        else:
            requiredParameters[requiredParameterName] = theValue
    #requiredParameters[str("userID")] = userInfo[str("id")]
    return(IDInfo, requiredParameters)

@app.route("/googleTokenSignin", methods=["POST"])
def googleTokenSignin():
    """
    Verify that a ID Token given by a client device is valid, and make sure the relevent user ID and home folder, etc, exists for
    that user. This is for authentication of user logins to the site.
    """
    # Do the verification - if a string is returned, that's an error, but otherwise
    # we should have the user's information, including their user ID.
    IDInfo = verifyGoogleIDToken(flask.request.values.get('idToken', None))
    if not isinstance(IDInfo, str):
        return "OK"
    return IDInfo
    
#@app.route("/authoriseGoogleAPI", methods=["POST"])
#def authoriseGoogleAPI():
#    """
#    The server-side function that initiates offline authentication for the site to use a given Google API. This (as far as this server is concerned) is a two-step process - this function
#    does a call to a remote function over HTTPS and gets back a URL to pass to the user. The user does stuff on Google's site (clicks "Okay, I approve this site", or whatever), then Google does
#    a call over HTTPS to the googleOAuth2Callback function below. State is tracked using a state code generated by Google (for now, could change that) used to store a Flow object in the googleFlowObjects global dict.
#    """
#    try:
#        (userInfo, parameters) = checkParameters(flask.request.values, ["service", "tokenName", "jobID"])
#    except ValueError as theError:
#        return "Error: " + str(theError)
#    if parameters["service"] == "googleDrive":
#        # Use the client_secret.json file to identify the application requesting authorization. The client ID (from that file) and access scopes are required.
#        #flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file("/var/www/sansay/client_secret.json", scopes=["https://www.googleapis.com/auth/drive"], redirect_uri="https://<<HOSTNAME>>/api/googleOAuth2Callback")
#        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file("/var/www/sansay/client_secret.json", scopes=["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/drive.metadata.readonly","https://www.googleapis.com/auth/plus.me"], redirect_uri="https://<<HOSTNAME>>/api/googleOAuth2Callback")
#        # Generate URL for request to Google's OAuth 2.0 server. We let Google generate a random state code for the moment - we could pass our own state code, made up of a hash of the user ID or similar, to better confirm that the corresponding
#        # call back is generated from the same browser.
#        authorization_url, state = flow.authorization_url(access_type="offline", prompt="consent", include_granted_scopes="true")
#        # Place the flow object in the database, persistent over HTTP requests, so it's retrievable later via the state code.
#        queryDB("INSERT INTO googleAuthFlowCache (state, flow, oAuth2SessionDict, userInfo, parameters) VALUES (?,?,?,?,?);", [state, pickle.dumps(flow), pickle.dumps({"_client":flow.oauth2session._client,"_state":flow.oauth2session._state,"redirect_uri":flow.oauth2session.redirect_uri,"compliance_hook":flow.oauth2session.compliance_hook,"scope":flow.oauth2session.scope}), pickle.dumps({"id":userInfo[str("id")], "googleSub":userInfo[str("googleSub")], "googleHd":userInfo[str("googleHd")]}), pickle.dumps(parameters)])
#        return authorization_url

@app.route("/googleOAuth2Callback", methods=["GET"])
def googleOAuth2Callback():
    """
    OAuth2 callback endpoint - second step of the offline Google Oath2 authentication flow initiated above.
    We don't call checkParameters from this function, it's already been called in step one and the userInfo and parameters variables pushed into a cache
    for retreival via the "state" value. I'm assuming this "state" value (generated server-side at Google's end) is unique and un-guessable, which we might
    want to double-check at some point.
    """
    # Get the state code from the parameters passed in the URL.
    state = flask.request.values.get("state", None)
    # Get the flow,userInfo,parameters tuple - then remove it from the database, it's a one-time use object.
    queryResult = queryDB("SELECT * FROM googleAuthFlowCache WHERE state=?;", [state], True)
    flow = pickle.loads(queryResult[str("flow")])
    # For some reason, the fields of flow.oauth2session don't get pickled, so we have store each field as a value in a dict.
    oauth2sessionDict = pickle.loads(queryResult[str("oAuth2SessionDict")])
    flow.oauth2session._client = oauth2sessionDict["_client"]
    flow.oauth2session._state = oauth2sessionDict["_state"]
    flow.oauth2session.redirect_uri = oauth2sessionDict["redirect_uri"]
    flow.oauth2session.compliance_hook = oauth2sessionDict["compliance_hook"]
    flow.oauth2session.scope = oauth2sessionDict["scope"]
    userInfo = queryDB("SELECT * FROM users WHERE id=?;", [pickle.loads(queryResult[str("userInfo")])["id"]], True)
    parameters = pickle.loads(queryResult[str("parameters")])
    queryDB("DELETE FROM googleAuthFlowCache WHERE state=?", [state], True)
    # Swap the authorization code for OAuth access and refresh tokens.
    flow.fetch_token(authorization_response=flask.request.url)
    # Read in the existing job file data.
    jobJSON = json.loads(getFileContents(parameters["userFolder"] + os.sep + parameters["jobID"]), object_pairs_hook=collections.OrderedDict)
    # Modify the existing job data to include the new access token.
    jobJSON[parameters["tokenName"]] = {"access_token":flow.credentials.token,"token_type":"Bearer","tokenURI":flow.credentials._token_uri,"clientSecret":flow.credentials._client_secret,"IDToken":flow.credentials._id_token,"refreshToken":flow.credentials._refresh_token,"scopes":flow.credentials._scopes,"clientID":flow.credentials._client_id,"expiry":flow.credentials.expiry.strftime("%Y-%m-%dT%H:%M:%S.%f000Z")}
    # Write out the job file data to the same path, replacing the old data.
    putFileContents(parameters["userFolder"] + os.sep + parameters["jobID"], json.dumps(jobJSON))
    return "<html><head><script src='https://code.jquery.com/jquery-3.2.1.min.js' integrity='sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=' crossorigin='anonymous'></script><script>$(function() {close();});</script></head><body>You can now close this tab.</body></html>"

if __name__ == "__main__":
    app.run()
