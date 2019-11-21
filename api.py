# Standard Python libraries.
import os
import re
import cgi
import hashlib

# The Flask library.
import flask

SERVER_NAME = "manage.knightsbridgeschool.com"

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

@app.route("/")
def index():
    return "Hello world!"

if __name__ == "__main__":
    app.run()
