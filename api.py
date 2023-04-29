# Standard Python libraries.
import os
import subprocess
import urllib.request
import xml.etree.ElementTree

# The Flask web application framework.
import flask

pageTitle = "Guacamole"

app = flask.Flask(__name__, static_url_path="", static_folder="/var/www/html/favicon")

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
    if username == "":
        if os.path.isfile("/etc/remote-gateway/newUser.py"):
            newUserProcess = subprocess.run(["python3", "/etc/remote-gateway/newUser.py " + cloudflareUsername], stdout=subprocess.PIPE)
            newUserResult = newUserProcess.decode("utf-8").split(",")
            if len(newUserResult) == 2:
                username = newUserResult[0]
                password = newUserResult[1]
                newUserXML = xml.etree.ElementTree.fromstring(getFile("/etc/remote-gateway/newUser.xml").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password))
                guacXML.append(newUserXML)
                putFile("/etc/guacamole/user-mapping.xml",  ElementTree.tostring(guacXML, encoding="utf8", method="xml"))
                
    return getFile("/var/www/html/client.html").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password).replace("<<CONNECTIONTITLE>>", pageTitle)

if __name__ == "__main__":
    app.run()
