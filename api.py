# Standard Python libraries.
import os

# The Flask web application framework.
import flask

app = flask.Flask(__name__)

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


@app.route("/", methods=["GET", "POST"])
def api():
    emailAddress = flask.request.values.get("email", None)
    pageName = flask.request.values.get("page", None)
    loginToken = flask.request.values.get("token", None)
    clientURL = "/guacamole/#/client/" + "TWFuYWdlMDAxAGMAZGVmYXVsdA" + "==?username=" + emailAddress + "&password=" + loginToken
    return clientURL

if __name__ == "__main__":
    app.run()
