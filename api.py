# Standard Python libraries.
import os
import urllib.request
import xml.etree.ElementTree

# The Flask web application framework.
import flask

app = flask.Flask(__name__)

def getFile(theFilename):
    fileDataHandle = open(theFilename, encoding="latin-1")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

@app.route("/", methods=["GET", "POST"])
def root():
    username = ""
    guacXML = xml.etree.ElementTree.fromstring(getFile("/etc/guacamole/user-mapping.xml"))
    for authorizeNode in guacXML.findall("./<user-mapping/authorize"):
        username = username + authorizeNode.text
    #username = flask.request.headers.get("Cf-Access-Authenticated-User-Email").split("@")[0]
    password = "bananas"
    return getFile("/var/www/html/client.html").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password).replace("<<CONNECTIONTITLE>>", "Guacamole")

if __name__ == "__main__":
    app.run()
