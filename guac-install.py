#!/usr/bin/python3

import os
import sys
import shutil
#import hashlib
import random

# Parse any options set by the user on the command line.
validBooleanOptions = []
validValueOptions = ["-serverName","-databasePassword","-guacPassword"]
userOptions = {}
optionCount = 1
while optionCount < len(sys.argv):
    if sys.argv[optionCount] in validBooleanOptions:
        userOptions[sys.argv[optionCount]] = True
    elif sys.argv[optionCount] in validValueOptions:
        userOptions[sys.argv[optionCount]] = sys.argv[optionCount+1]
        optionCount = optionCount + 1
    optionCount = optionCount + 1

def runIfPathMissing(thePath, theCommand):
    if not os.path.exists(thePath):
        print("Running: " + theCommand)
        os.system(theCommand)
        
def copyfile(src, dest, mode=None):
    srcStat = os.stat(src)
    if (not os.path.exists(dest)) or (not str(srcStat.st_mtime) == str(os.stat(dest).st_mtime)):
        print("Copying file " + src + " to " + dest)
        shutil.copyfile(src, dest)
        os.utime(dest, (srcStat.st_atime, srcStat.st_mtime))
        if not mode == None:
            os.system("chmod " + mode + " " + dest)
        return(1)
    return(0)

def getUserOption(optionName, theMessage):
    if not optionName in userOptions.keys():
        userOptions[optionName] = input(theMessage + ": ")
    return(userOptions[optionName])

def readFile(theFilename):
    fileDataHandle = open(theFilename, "r")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)
    
def writeFile(theFilename, theFileData):
    fileDataHandle = open(theFilename, "w")
    if isinstance(theFileData, list):
        fileDataHandle.write("\n".join(theFileData))
    else:
        fileDataHandle.write(theFileData)
    fileDataHandle.close()
    
def replaceVariables(theFile, theKeyValues):
    fileData = readFile(theFile)
    for keyValue in theKeyValues.keys():
        fileData = fileData.replace("<<" + keyValue + ">>", theKeyValues[keyValue])
    writeFile(theFile, fileData)

# First, get some needed values from the user, if they haven't already provided them on the command line.
print("Installing...")
getUserOption("-serverName", "Please enter this server's full name (e.g. server.domain.com)")
getUserOption("-databasePassword", "Please enter the password to set for Guacamole's database")
getUserOption("-guacPassword", "Please enter the password to set for Guacamole")

# Use Chase Wright's script to install a Guacamole server - see: https://github.com/MysticRyuujin/guac-install
if not os.path.exists(os.getenv("HOME") + os.sep + "guac-install.sh"):
    os.system("cd ~; wget https://git.io/fxZq5 -O guac-install.sh")
    os.system("cd ~; chmod +x guac-install.sh")
    os.system("cd ~; ./guac-install.sh --mysqlpwd " + userOptions["-databasePassword"] + " --guacpwd " + userOptions["-guacPassword"] + " --nomfa --installmysql")

# Make sure Pip3 (Python 3 package manager) is installed.
runIfPathMissing("/usr/bin/pip3", "apt-get install -y python3-pip")

# Figure out what version of Python3 we have installed.
pythonVersion = os.popen("ls /usr/local/lib | grep python3").read().strip()

# Make sure Git (source code control client) is installed.
runIfPathMissing("/usr/bin/git", "apt-get install -y git")

# Make sure curl (utility to get files from the web) is installed.
runIfPathMissing("/usr/bin/curl", "apt-get install -y curl")

# Make sure build-essential (Debian build environment, should include most tools you need to build other packages) is installed.
runIfPathMissing("/usr/share/doc/build-essential", "apt-get install -y build-essential")

# Make sure SSHPass (used to allow passwords to be passed into SSH) is installed.
runIfPathMissing("/usr/share/doc/sshpass", "apt-get install -y sshpass")



# Make sure Flask (Python web-publishing framework, used for the "/api" namespace) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/flask", "pip3 install flask")

# Make sure XLRD (Python library for handling Excel files, required for Excel support in Pandas) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/xlrd", "pip3 install xlrd")

# Make sure OpenPyXL (Python library for handling Excel files, required for Excel support in Pandas) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/openpyxl", "pip3 install openpyxl")

# Make sure Pandas (Python data-analysis library) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/pandas", "pip3 install pandas")

# Make sure Numpy (Python maths library) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/numpy", "pip3 install numpy")



# Make sure the Nginx web/proxy server is installed (used to proxy the Tomcat server and provide SSL)...
runIfPathMissing("/usr/share/doc/nginx", "apt-get install -y nginx")
# ...with support for Let's Encrypt. See here:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-10
# Also, see later section on crontab for monthly certbot renew / backup process.
runIfPathMissing("/usr/lib/python3/dist-packages/certbot", "apt-get install -y python3-acme python3-certbot-nginx python3-mock python3-openssl python3-pkg-resources python3-pyparsing python3-zope.interface")
# Make sure uWSGI (WSGI component for Nginx) is installed...
runIfPathMissing("/usr/local/bin/uwsgi", "pip3 install uwsgi")
# ...and copy over the WSGI-based API configuration and code.
copyfile("emperor.uwsgi.service", "/etc/systemd/system/emperor.uwsgi.service", mode="0755")
copyfile("api.py", "/var/lib/nginx/uwsgi/api.py", mode="0755")
copyfile("client.html", "/var/www/html/client.html", mode="0755")
copyfile("error.html", "/var/www/html/error.html", mode="0755")

# Make sure Webconsole is installed and that a task to trigger a data import is set up.
validChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
if os.path.exists("/etc/webconsole/tasks"):
    taskID = os.listdir("/etc/webconsole/tasks")[0]
else:
    taskID = ""
    for pl in range (0,16):
        taskID = taskID + validChars[random.randint(0,len(validChars)-1)]
    # Install Webconsole.
    os.system("curl -s https://www.sansay.co.uk/web-console/install.sh | bash")
    os.system("mkdir /etc/webconsole/tasks/" + taskID)
copyfile("config.txt", "/etc/webconsole/tasks/" + taskID + "/config.txt", mode="0755")
copyfile("syncData.sh", "/etc/webconsole/tasks/" + taskID + "/syncData.sh", mode="0755")

# Make sure UFW (Debian firewall) is installed.
runIfPathMissing("/usr/share/doc/ufw", "apt-get install -y ufw")
# Set up firewall rules - allow HTTP and HTTPS from external IP addresses, but only allow Tomcat's port 8080 from localhost.
os.system("ufw allow http > /dev/null 2>&1")
os.system("ufw allow https > /dev/null 2>&1")
os.system("echo y | ufw enable > /dev/null 2>&1")

print("Stopping Guacamole...")
os.system("systemctl stop guacd")
print("Stopping Tomcat...")
os.system("systemctl stop tomcat9")
print("Stopping uWSGI...")
os.system("systemctl stop emperor.uwsgi.service")
print("Stopping Nginx...")
os.system("systemctl stop nginx")
# Make sure the (blank) Guacamole user-mapping file exists.
os.system("echo > /etc/guacamole/user-mapping.xml")
os.system("chmod a+rwx /etc/guacamole/user-mapping.xml")
# Enable the uWSGI server service.
os.system("systemctl enable emperor.uwsgi.service > /dev/null 2>&1")
# Copy over the Nginx config files.
os.system("cp nginx.conf /etc/nginx/nginx.conf")
# If not already done so, set up an HTTPS certificate using Let's Encrypt.
if os.path.isfile("/etc/letsencrypt/live/" + userOptions["-serverName"] + "/fullchain.pem"):
    os.system("cp default /etc/nginx/sites-available/default")
    replaceVariables("/etc/nginx/sites-available/default", {"SERVERNAME":userOptions["-serverName"]})
else:
    os.system("cp default-noSSL /etc/nginx/sites-available/default")
    replaceVariables("/etc/nginx/sites-available/default", {"SERVERNAME":userOptions["-serverName"]})
    print("Starting Nginx...")
    os.system("systemctl start nginx")
    print("Running certbot...")
    os.system("certbot")
    print("Re-run install.py to use new SSL certificates...")
    os.system("python3 guac-install.py -serverName " + userOptions["-serverName"] + " -databasePassword " + userOptions["-databasePassword"] + " -guacPassword " + userOptions["-guacPassword"])
    sys.exit(0)
print("Starting Nginx...")
os.system("systemctl start nginx")
print("Starting uWSGI...")
os.system("systemctl start emperor.uwsgi.service")
print("Starting Tomcat...")
os.system("systemctl start tomcat9")
print("Starting Guacamole server...")
os.system("systemctl start guacd")

# Set up Cron.
copyfile("crontab", "/var/spool/cron/crontabs/root", mode="0600")
os.system("cp monthlyCronjob.sh /etc/guacamole")
os.system("chmod u+x /etc/guacamole/monthlyCronjob.sh")
os.system("/etc/init.d/cron restart")

# Print out some useful information.
print("Webconsole Task URL: https://" + userOptions["-serverName"] + "/console/view?taskID=" + taskID)