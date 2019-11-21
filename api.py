# Standard Python libraries.
import os
import re
import cgi
import sys
import hashlib

# The Flask library.
import flask

def flushPrint(theString):
    print(theString + "\n")
    sys.stdout.flush()

flushPrint("Imported Flask.")

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
    flushPrint("In index.")
    return "Hello world!"

if __name__ == "__main__":
    flushPrint("Started main.")
    app.run()
