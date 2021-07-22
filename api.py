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
    fileDataHandle.write(fileData)
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
        for item in os.listdir("/etc/guacamole/connections"):
            itemRead = false
            if item.endswith(".csv"):
                itemData = pandas.read_csv("/etc/guacamole/connections/" + item, header=0)
                itemRead = True
            if item.endswith(".xlsx"):
                itemData = pandas.read_excel("/etc/guacamole/connections/" + item, header=0)
                itemRead = True
            if itemRead:
                clientURL = clientURL + "BANANAS"
            return getFile("/var/www/html/client.html").replace("<<CLIENTURLGOESHERE>>", clientURL)
    return getFile("/var/www/html/error.html").replace("<<ERRORMESSAGEGOESHERE>>", errorMessage)

if __name__ == "__main__":
    app.run()
