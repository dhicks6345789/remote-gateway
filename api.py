# Standard Python libraries.
import os
import urllib.request

# The Flask web application framework.
import flask

# Pandas
import pandas

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
def api():
    errorMessage = ""
    emailAddress = flask.request.values.get("email", None)
    if emailAddress == None:
        errorMessage = "ERROR: Missing email field."
    pageName = flask.request.values.get("page", None)
    if pageName == None:
        errorMessage = "ERROR: Missing page field."
    loginToken = flask.request.values.get("token", None)
    if loginToken == None:
        errorMessage = "ERROR: Missing token field."
    if errorMessage == "":
        # Check we have a valid login, not just some random values passed in.
        queryURL = "https://dev.mystart.online/api/validateToken?loginToken=" + loginToken + "&pageName=" + pageName
        try:
            validationResponse = urllib.request.urlopen(queryURL)
            responseContent = validationResponse.read().decode("latin-1", "ignore").strip()
            if responseContent.startswith("VALID:"):
                if responseContent.split(":")[1] != emailAddress:
                    errorMessage = "ERROR: Email address doesn't match login token."
            else:
                errorMessage = "ERROR: Invalid login token / page name."
        except urllib.error.HTTPError as err:
            errorMessage = "ERROR: URL " + queryURL + " gives error " + err.reason
            
    if errorMessage == "":
        clientURL = "/guacamole/#/client?username=" + emailAddress + "&password=" + loginToken
        
        hosts = {}
        for item in os.listdir("/etc/guacamole/hosts"):
            itemRead = False
            if item.endswith(".csv"):
                itemData = pandas.read_csv("/etc/guacamole/hosts/" + item, header=None)
                itemRead = True
            if item.endswith(".xlsx"):
                itemData = pandas.read_excel("/etc/guacamole/hosts/" + item, header=None)
                itemRead = True
            if itemRead:
                for hostDataIndex, hostData in itemData.iterrows():
                    if hostData[0].lower() != "host":
                        hosts[hostData[0].lower()] = [hostData[1],hostData[2],hostData[3],hostData[4]]
        
        connections = []
        for item in os.listdir("/etc/guacamole/connections"):
            itemRead = False
            if item.endswith(".csv"):
                itemData = pandas.read_csv("/etc/guacamole/connections/" + item, header=None)
                itemRead = True
            if item.endswith(".xlsx"):
                itemData = pandas.read_excel("/etc/guacamole/connections/" + item, header=None)
                itemRead = True
            if itemRead:
                for connectionDataIndex, connectionData in itemData.iterrows():
                    if connectionData[0].lower() != "host":
                        if emailAddress.lower() == connectionData[1].lower():
                            connections.append([connectionData[0],connectionData[1].lower()])
        xmlData = ""
        if os.path.exists("/etc/guacamole/user-mapping.xml"):
            xmlData = getFile("/etc/guacamole/user-mapping.xml").strip()
        if xmlData != "":
            xmlData = xmlData + "\n"
            
        # To do - properly check if some existing data needs to be kept.
        xmlData = ""
        
        xmlData = xmlData + "<user-mapping>\n"
        xmlData = xmlData + "\t<authorize username=\"" + emailAddress.lower() + "\" password=\"" + loginToken + "\">\n"
        for connection in connections:
            host = hosts[connection[0].lower()]
            #os.system("sshpass -p " + host[2] + " ssh -o \"StrictHostKeyChecking=no\" " + host[0] + " \"" + host[3].replace("<<KEY>>", loginToken) + "\"")
            xmlData = xmlData + "\t\t<connection name=\"" + connection[0] + "\">\n"
            protocol = host[1].lower()
            xmlData = xmlData + "\t\t\t<protocol>" + protocol + "</protocol>\n"
            xmlData = xmlData + "\t\t\t<param name=\"hostname\">" + host[0].split("@")[1] + "</param>\n"
            if protocol == "vnc":
                xmlData = xmlData + "\t\t\t<param name=\"port\">5900</param>\n"
            elif protocol == "rdp":
                xmlData = xmlData + "\t\t\t<param name=\"port\">3389</param>\n"
                xmlData = xmlData + "\t\t\t<param name=\"domain\">" + host[3] + "</domain>\n"
                xmlData = xmlData + "\t\t\t<param name=\"security\">nla</param>\n"
                xmlData = xmlData + "\t\t\t<param name=\"ignore-cert\">true</param>\n"
            xmlData = xmlData + "\t\t\t<param name=\"password\">" + host[2] + "</param>\n"
            xmlData = xmlData + "\t\t</connection>\n"
        xmlData = xmlData + "\t</authorize>\n"
        xmlData = xmlData + "</user-mapping>\n"
        putFile("/etc/guacamole/user-mapping.xml", xmlData)
        return getFile("/var/www/html/client.html").replace("<<CONNECTIONURL>>", clientURL).replace("<<CONNECTIONTITLE>>", connection[0])
    
    return getFile("/var/www/html/error.html").replace("<<CONNECTIONERROR>>", errorMessage).replace("<<CONNECTIONTITLE>>", "Guacamole")

if __name__ == "__main__":
    app.run()
