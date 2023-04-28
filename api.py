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
    return flask.Response(getBinaryFile("/var/www/html/apple-touch-icon.png"), mimetype="image/x-png")

@app.route("/favicon-32x32.png", methods=["GET"])
def getFavicon32x32():
    return flask.Response(getBinaryFile("/var/www/html/favicon-32x32.png"), mimetype="image/x-png")

@app.route("/favicon-16x16.png", methods=["GET"])
def getFavicon16x16():
    return flask.Response(getBinaryFile("/var/www/html/favicon-16x16.png"), mimetype="image/x-png")

@app.route("/site.webmanifest", methods=["GET"])
def getSite.Webmanifest():
    return flask.Response(getBinaryFile("/var/www/html/site.webmanifest"), mimetype="application/manifest+json")

@app.route("/safari-pinned-tab.svg", methods=["GET"])
def getSafariPinnedTab():
    return flask.Response(getBinaryFile("/var/www/html/safari-pinned-tab.svg"), mimetype="image/svg+xml")

if __name__ == "__main__":
    app.run()
