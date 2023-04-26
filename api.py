# Standard Python libraries.
import os
import urllib.request

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
    fileDataHandle.write(theData)
    fileDataHandle.close()

def runCommand(theCommand):
    commandHandle = os.popen(theCommand)
    result = commandHandle.read()
    commandHandle.close()
    return(result)

@app.route("/", methods=["GET", "POST"])
def root():
    return getFile("/var/www/html/client.html")
    #.replace("<<CONNECTIONERROR>>", errorMessage).replace("<<CONNECTIONTITLE>>", "Guacamole")

if __name__ == "__main__":
    app.run()
