# Standard Python libraries.
import os
import random
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

def putFile(theFilename, theData):
    fileDataHandle = open(theFilename, "wb")
    fileDataHandle.write(theData.encode("latin-1"))
    fileDataHandle.close()

def getBinaryFile(theFilename):
    fileDataHandle = open(theFilename, mode="rb")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

passChars = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def generatePassword():
    result = ""
    for pl in range(0, 32):
        result = result + passChars[random.randint(0, len(passChars)-1)]
    return result

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
            newUserProcess = subprocess.run(["python3", "/etc/remote-gateway/newUser.py", cloudflareUsername, generatePassword()], stdout=subprocess.PIPE)
            newUserResult = newUserProcess.stdout.decode("utf-8").split(",")
            if len(newUserResult) == 2:
                username = newUserResult[0]
                password = newUserResult[1]
                newUserXML = xml.etree.ElementTree.fromstring(getFile("/etc/remote-gateway/newUser.xml").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password))
                guacXML.append(newUserXML)
                putFile("/etc/guacamole/user-mapping.xml",  xml.etree.ElementTree.tostring(guacXML, encoding="utf8", method="xml"))
                
    return getFile("/var/www/html/client.html").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password).replace("<<CONNECTIONTITLE>>", pageTitle)

if __name__ == "__main__":
    app.run()
