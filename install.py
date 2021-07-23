#!/usr/bin/python3

import os
import sys
import shutil
import hashlib
import random

# Parse any options set by the user on the command line.
validBooleanOptions = []
validValueOptions = ["-serverName"]
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
    
def runExpect(inputArray):
    writeFile("temp.expect", inputArray)
    os.system("expect temp.expect")
    os.system("rm temp.expect")



# First, get some needed values from the user, if they haven't already provided them on the command line.
print("Installing...")
getUserOption("-serverName", "Please enter this server's full name (e.g. server.domain.com)")
#getUserOption("-databasePassword", "Please enter the password to set for Guacamole's database")



# Make sure dos2unix (line-end conversion utility) is installed.
runIfPathMissing("/usr/bin/dos2unix", "apt-get install -y dos2unix")

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

# Make sure ZLib (compression library, required for building other packages) is installed.
runIfPathMissing("/usr/share/doc/zlib1g-dev", "apt-get install -y zlib1g-dev")

# Make sure Expect (command-line automation utility) is installed.
runIfPathMissing("/usr/bin/expect", "apt-get -y install expect")

# Make sure the Java Development Kit (JDK, used for compiling Java applications) is installed.
runIfPathMissing("/usr/share/doc/default-jdk", "apt-get install -y default-jdk")



# Make sure Cairo (library used by Guacamole for rendering graphics) is installed.
runIfPathMissing("/usr/share/doc/libcairo2-dev", "apt-get install -y libcairo2-dev")

# Make sure libjpeg62-turbo-dev (library used by Guacamole for handling JPEG image data) is installed.
runIfPathMissing("/usr/share/doc/libjpeg62-turbo-dev", "apt-get install -y libjpeg62-turbo-dev")

# Make sure libpng-dev (library used by Guacamole for handling PNG image data) is installed.
runIfPathMissing("/usr/share/doc/libpng-dev", "apt-get install -y libpng-dev")

# Make sure libossp-uuid-dev (library used by Guacamole for handling PNG image data) is installed.
runIfPathMissing("/usr/share/doc/libossp-uuid-dev", "apt-get install -y libossp-uuid-dev")

# Make sure FFmpeg (library used by Guacamole for handling video encoding) is installed.
runIfPathMissing("/usr/share/doc/libavcodec-dev", "apt-get install -y libavcodec-dev")
runIfPathMissing("/usr/share/doc/libavutil-dev", "apt-get install -y libavutil-dev")
runIfPathMissing("/usr/share/doc/libswscale-dev", "apt-get install -y libswscale-dev")

# Make sure FreeRDP (library used by Guacamole to handle RDP connections) is installed.
# Note that, hopefully, in a future version of Gaucamole, this dependancy is going to
# change from libfreerdp-dev to freerdp2-dev. For the moment, we have to include Debian
# Stretch repositories to be able to install libfreerdp-dev.
#runIfPathMissing("/usr/share/doc/libfreerdp-dev", "apt-get install -y libfreerdp-dev")
runIfPathMissing("/usr/share/doc/freerdp2-dev", "apt-get install -y freerdp2-dev")

# Make sure Pango (library used by Guacamole to support SSH and Telnet connections) is installed.
runIfPathMissing("/usr/share/doc/libpango1.0-dev", "apt-get install -y libpango1.0-dev")

# Make sure libssh2 (library used by Guacamole to support SSH connections) is installed.
runIfPathMissing("/usr/share/doc/libssh2-1-dev", "apt-get install -y libssh2-1-dev")

# Make sure libtelnet (library used by Guacamole to support Telnet connections) is installed.
runIfPathMissing("/usr/share/doc/libtelnet-dev", "apt-get install -y libtelnet-dev")

# Make sure libvncserver (library used by Guacamole to support VNC connections) is installed.
runIfPathMissing("/usr/share/doc/libvncserver-dev", "apt-get install -y libvncserver-dev")

# Make sure Pulse Audio (library used by Guacamole to support audio over VNC) is installed.
runIfPathMissing("/usr/share/doc/libpulse-dev", "apt-get install -y libpulse-dev")

# Make sure libssl (library used by Guacamole to support SSL) is installed.
runIfPathMissing("/usr/share/doc/libssl-dev", "apt-get install -y libssl-dev")

# Make sure Ogg Vorbis (library used by Guacamole to support Ogg Vorbis audio) is installed.
runIfPathMissing("/usr/share/doc/libvorbis-dev", "apt-get install -y libvorbis-dev")

# Make sure libwebp (library used by Guacamole to support WebP image data) is installed.
runIfPathMissing("/usr/share/doc/libwebp-dev", "apt-get install -y libwebp-dev")



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



# Make sure the Tomcat servlet container is installed (used for serving Guacamole client contents to users connecting to the Guacamole server via the web).
runIfPathMissing("/usr/share/doc/tomcat9", "apt-get install -y tomcat9 tomcat9-admin tomcat9-common tomcat9-user")

# Make sure the Nginx web/proxy server is installed (used to proxy the Tomcat server and provide SSL)...
runIfPathMissing("/usr/share/doc/nginx", "apt-get install -y nginx")
# ...with support for Let's Encrypt. See here:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-10
# Also, see later section on crontab for monthly certbot renew / backup process.
runIfPathMissing("/usr/lib/python3/dist-packages/certbot", "apt-get install -y python3-acme python3-certbot-nginx python3-mock python3-openssl python3-pkg-resources python3-pyparsing python3-zope.interface")
# Make sure uWSGI (WSGI component for Nginx) is installed.
runIfPathMissing("/usr/local/bin/uwsgi", "pip3 install uwsgi")
copyfile("emperor.uwsgi.service", "/etc/systemd/system/emperor.uwsgi.service", mode="0755")
copyfile("api.py", "/var/lib/nginx/uwsgi/api.py", mode="0755")
copyfile("client.html", "/var/www/html/client.html", mode="0755")
copyfile("error.html", "/var/www/html/error.html", mode="0755")

# Make sure the Webconsole task to trigger a data import is set up.
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

# Make sure UFW is installed (Debian firewall).
runIfPathMissing("/usr/share/doc/ufw", "apt-get install -y ufw")
# Set up firewall rules - allow HTTP and HTTPS from external IP addresses, but only allow Tomcat's port 8080 from localhost.
os.system("ufw allow OpenSSH > /dev/null 2>&1")
os.system("ufw allow http > /dev/null 2>&1")
os.system("ufw allow https > /dev/null 2>&1")
os.system("echo y | ufw enable > /dev/null 2>&1")

# Make sure Guacamole's config folders exist.
runIfPathMissing("/etc/guacamole", "mkdir /etc/guacamole")
runIfPathMissing("/etc/guacamole/extensions", "mkdir /etc/guacamole/extensions")
runIfPathMissing("/etc/guacamole/lib", "mkdir /etc/guacamole/lib")

# Make sure MariaDB (used by Guacamole for user management) is installed.
# See: https://guacamole.apache.org/doc/gug/jdbc-auth.html#jdbc-auth-installation
#if not os.path.exists("/usr/share/doc/mariadb-server"):
#    os.system("apt-get install -y mariadb-server")
#    print("Configuring MariaDB...")
#    runExpect([
#        "spawn /usr/bin/mysql_secure_installation",
#        "expect \"(enter for none):\"",
#        "send \"\\r\"",
#        "expect \"\\[Y/n\\]\"",
#        "send \"n\\r\"",
#        "expect \"\\[Y/n\\]\"",
#        "send \"y\\r\"",
#        "expect \"\\[Y/n\\]\"",
#        "send \"y\\r\"",
#        "expect \"\\[Y/n\\]\"",
#        "send \"y\\r\"",
#        "expect \"\\[Y/n\\]\"",
#        "send \"y\\r\"",
#        "interact"
#    ])
#    # Create the mysql Guacamole database (guacamole_db).
#    os.system("echo \"CREATE DATABASE guacamole_db;\" | mysql")
#    # Create the mysql Guacamole user (guacamole_user).
#    os.system("echo \"CREATE USER 'guacamole_user'@'localhost' IDENTIFIED BY '" + userOptions["-databasePassword"] + "'; FLUSH PRIVILEGES;\" | mysql")
#    os.system("echo \"GRANT CREATE,SELECT,INSERT,UPDATE,DELETE ON guacamole_db.* TO 'guacamole_user'@'localhost'; FLUSH PRIVILEGES;\" | mysql")
#    # Set up Guacamole's database using the provided schema.
#    os.system("cat guacamole-auth-jdbc-1.0.0/mysql/schema/*.sql | mysql -u guacamole_user -p" + userOptions["-databasePassword"] + " guacamole_db")
#    
#    # Copy over the Guacamole database authentication extension.
#    os.system("cp guacamole-auth-jdbc-1.0.0/mysql/guacamole-auth-jdbc-mysql-1.0.0.jar /etc/guacamole/extensions")
#    # Obtain, extract and install the MySQL JDBC connector.
#    runIfPathMissing("mysql-connector-java_8.0.18-1debian10_all.deb", "wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java_8.0.18-1debian10_all.deb; mkdir temp; cd temp; ar x ../mysql-connector-java_8.0.18-1debian10_all.deb; tar xf data.tar.xz; cp usr/share/java/mysql-connector-java-8.0.18.jar /etc/guacamole/lib; cd ..; rm -rf temp")
#    # Copy over the Guacamole configuration file.
#    os.system("cp guacamole.properties /etc/guacamole")
#    replaceVariables("/etc/guacamole/guacamole.properties", {"DATABASEPASSWORD":userOptions["-databasePassword"]})

## Make sure Maven is installed (Apche's build tool, used to build the Java-based Guacamole authentication extension).
#runIfPathMissing("/usr/share/doc/maven", "apt-get install -y maven")

## Set up the Maven project to build the custom Guacamole authentication provider.
#os.makedirs("src/main/java/org/apache/guacamole/auth", exist_ok=True)
#os.system("cp MystartAuthenticationProvider.java src/main/java/org/apache/guacamole/auth")
#os.makedirs("src/main/resources", exist_ok=True)
#os.system("cp guac-manifest.json src/main/resources")
## Build the extension.
#runIfPathMissing("target/guacamole-auth-mystart-1.0.0.jar", "mvn package")
# Install the extension.
#os.system("cp target/guacamole-auth-mystart-1.0.0.jar /etc/guacamole/extensions")



print("Stopping Guacamole...")
os.system("systemctl stop guacd")
print("Stopping Tomcat...")
os.system("systemctl stop tomcat9")
print("Stopping uWSGI...")
os.system("systemctl stop emperor.uwsgi.service")
print("Stopping Nginx...")
os.system("systemctl stop nginx")
# Build and install Guacamole.
runIfPathMissing("guacamole-server-1.3.0", "tar -xzf guacamole-server-1.3.0.tar.gz; cd guacamole-server-1.3.0; ./configure --enable-allow-freerdp-snapshots --with-init-dir=/etc/init.d; make; make install; ldconfig -v; cd ..")
#runIfPathMissing("guacamole-auth-jdbc-1.0.0", "tar -xzf guacamole-auth-jdbc-1.0.0.tar.gz; cd guacamole-auth-jdbc-1.0.0; cd ..")
# Make sure the (blank) Guacamole user-mapping file exists.
os.system("echo > /etc/guacamole/user-mapping.xml")
os.system("chmod a+rwx /etc/guacamole/user-mapping.xml")
# Enable the Guacamole server service.
os.system("systemctl enable guacd > /dev/null 2>&1")
# Enable the uWSGI server service.
os.system("systemctl enable emperor.uwsgi.service > /dev/null 2>&1")
# Copy over the Nginx config files.
os.system("cp nginx.conf /etc/nginx/nginx.conf")
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
    print("STOPPING: Re-run install.py to use new SSL certificates.")
    sys.exit(0)
# Copy over the Tomcat config files.
os.system("cp tomcat9 /etc/default/tomcat9")
os.system("cp server.xml /usr/share/tomcat9/skel/conf/server.xml")
# Copy over the Guacamole client (pre-compiled Java servlet)...
os.system("cp guacamole-1.3.0.war /etc/guacamole/guacamole.war")
runIfPathMissing("/var/lib/tomcat9/webapps/guacamole.war", "ln -s /etc/guacamole/guacamole.war /var/lib/tomcat9/webapps/")
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
os.system("dos2unix monthlyCronjob.sh > /dev/null 2>&1")
os.system("cp monthlyCronjob.sh /etc/guacamole")
os.system("chmod u+x /etc/guacamole/monthlyCronjob.sh")
os.system("/etc/init.d/cron restart")

# Print out some useful information.
print("Webconsole Task URL: https://" + userOptions["-serverName"] + "/console/view?taskID=" + taskID)
