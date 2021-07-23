# Standard Python libraries.
import os

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
        clientURL = "/guacamole/#/client/" + "TWFuYWdlMDAxAGMAZGVmYXVsdA" + "==?username=" + emailAddress + "&password=" + loginToken
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
                    if connectionData[0].lower() != "address":
                        if emailAddress.lower() == connectionData[3].lower():
                            connections.append([connectionData[0],connectionData[1],connectionData[2],connectionData[3].lower()])
        xmlData = ""
        if os.path.exists("/etc/guacamole/user-mapping.xml"):
            xmlData = getFile("/etc/guacamole/user-mapping.xml").strip()
        if xmlData != "":
            xmlData = xmlData + "\n"
        # To do - properly check if some existing data needs to be kept.
        xmlData = ""
        
        xmlData = xmlData + "<authorize username=\"" + emailAddress.lower() + "\" password=\"" + loginToken + "\">\n"
        for connection in connections:
            xmlData = xmlData + "\t<connection name=\"" + connection[1] + "\">"
            xmlData = xmlData + "\t\t<protocol>vnc</protocol>\n"
            xmlData = xmlData + "\t\t<param name=\"hostname\">" + connection[0] + "</param>\n"
            xmlData = xmlData + "\t\t<param name=\"port\">5900</param>\n"
            xmlData = xmlData + "\t\t<param name=\"password\">" + loginToken + "</param>\n"
            xmlData = xmlData + "\t</connection>"
        xmlData = xmlData + "</authorize>\n"
        putFile("/etc/guacamole/user-mapping.xml", xmlData)
        return getFile("/var/www/html/client.html").replace("<<CLIENTURLGOESHERE>>", clientURL)
    return getFile("/var/www/html/error.html").replace("<<ERRORMESSAGEGOESHERE>>", errorMessage)

if __name__ == "__main__":
    app.run()
