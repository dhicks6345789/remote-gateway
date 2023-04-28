# Standard Python libraries.
import os
import urllib.request
import xml.etree.ElementTree

# The Flask web application framework.
import flask

pageTitle = "Guacamole"

app = flask.Flask(__name__)

def getFile(theFilename):
    fileDataHandle = open(theFilename, encoding="latin-1")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

def getBinaryFile(theFilename):
    fileDataHandle = open(theFilename, mode="rb")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

@app.route("/", methods=["GET", "POST"])
def root():
    cloudflareUsername = flask.request.headers.get("Cf-Access-Authenticated-User-Email").split("@")[0]
    
    username = ""
    password = ""
    guacXML = xml.etree.ElementTree.fromstring(getFile("/etc/guacamole/user-mapping.xml"))
    for childNode in guacXML:
        if childNode.tag == "authorize":
            if "username" in childNode.attrib.keys() and "password" in childNode.attrib.keys():
                if cloudflareUsername == childNode.attrib["username"]:
                    username = childNode.attrib["username"]
                    password = childNode.attrib["password"]
    return getFile("/var/www/html/client.html").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password).replace("<<CONNECTIONTITLE>>", pageTitle)

@app.route("/apple-touch-icon.png", methods=["GET"])
def getAppleTouchIcon():
    # return getBinaryFile("/var/www/html/apple-touch-icon.png")
    return flask.Response(getBinaryFile("/var/www/html/apple-touch-icon.png"), mimetype="image/x-png")

if __name__ == "__main__":
    app.run()
