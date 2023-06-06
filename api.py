# Standard Python libraries.
import os
import random
import socket
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
    fileDataHandle = open(theFilename, "w")
    fileDataHandle.write(theData)
    fileDataHandle.close()

def getBinaryFile(theFilename):
    fileDataHandle = open(theFilename, mode="rb")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

def getCommandOutput(theCommand):
    return(subprocess.check_output(theCommand, shell=True, text=True).rstrip().split("\n"))

passChars = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def generatePassword():
    result = ""
    for pl in range(0, 32):
        result = result + passChars[random.randint(0, len(passChars)-1)]
    return result

# Find the server's local IP address.
ipSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ipSocket.connect(("8.8.8.8", 80))
serverIPAddress = ipSocket.getsockname()[0]
ipSocket.close()

@app.route("/registerPi", methods=["GET", "POST"])
def registerPi():
    if flask.request.method == "GET":
        return getFile("/var/www/html/registerPi.sh").replace("{{SERVERIPADDRESS}}",serverIPAddress)
    else:
        piName = flask.request.form.get("piName")
        clientIPAddress = flask.request.remote_addr
        arpCommandOutput = getCommandOutput("ping " + clientIPAddress + "-c 1; arp -a | grep " + clientIPAddress + " | grep -o '..:..:..:..:..:..'")
        clientMACAddress = arpCommandOutput[-1]
        users = {}
        for csvRow in getFile("/etc/guacamole/user-mapping.csv").rstrip().split("\n"):
            csvRowSplit = csvRow.split(",")
            users[csvRowSplit[0]] = csvRowSplit[1:]
        return "OK" + str(users)

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
                username = newUserResult[0].strip()
                password = newUserResult[1].strip()
                newUserXML = getFile("/etc/remote-gateway/newUser.xml").strip().replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password)
                guacXMLText = getFile("/etc/guacamole/user-mapping.xml").replace("<user-mapping>", "").replace("</user-mapping>", "").strip()
                if guacXMLText != "":
                    guacXMLText = guacXMLText + "\n"
                putFile("/etc/guacamole/user-mapping.xml",  "<user-mapping>\n" + guacXMLText + "    " + newUserXML + "\n</user-mapping>\n")
            else:
                return getFile("/var/www/html/error.html").replace("<<ERRORMESSAGE>>", "User " + cloudflareUsername + " not valid.").replace("<<CONNECTIONTITLE>>", pageTitle)
                
    return getFile("/var/www/html/client.html").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password).replace("<<CONNECTIONTITLE>>", pageTitle)

if __name__ == "__main__":
    app.run()
