# Standard Python libraries.
import os
import urllib.request

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
    username = flask.request.headers.get("Cf-Access-Authenticated-User-Email").split("@")[0]
    password = "bananas"
    return getFile("/var/www/html/client.html").replace("<<USERNAME>>", username).replace("<<PASSWORD>>", password).replace("<<CONNECTIONTITLE>>", "Guacamole")

if __name__ == "__main__":
    app.run()
