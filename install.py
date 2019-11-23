#!/usr/bin/python3

import os
import sys
import shutil
import hashlib

# Parse any options set by the user on the command line.
validBooleanOptions = []
validValueOptions = ["-serverName", "-googleClientID", "-googleClientSecret", "-adminPassword", "-remotePassword"]
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

print("Installing...")

getUserOption("-serverName", "Please enter this server's full name (e.g. server.domain.com)")
getUserOption("-googleClientID", "Please enter the Google Client ID used for the Log In With Google functionality")
getUserOption("-googleClientSecret", "Please enter the Google Client Secret used for the Log In With Google functionality")
getUserOption("-adminPassword", "Please enter the admin password for the remote server")
getUserOption("-remotePassword", "Please enter the password to use for Guacamole")

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
#runIfPathMissing("/usr/share/doc/libfreerdp-dev", "echo \"deb http://deb.debian.org/debian/ stretch main\" > /etc/apt/sources.list.d/temp-debian-stretch.list")
#runIfPathMissing("/usr/share/doc/libfreerdp-dev", "apt-get update; apt-get install -y libmysql-java libfreerdp-dev; rm /etc/apt/sources.list.d/temp-debian-stretch.list; apt-get update")
runIfPathMissing("/usr/share/doc/libfreerdp-dev", "apt-get install -y libfreerdp-dev")

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



# Make sure Flask (Python web-publishing framework) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/flask", "pip3 install flask")

# Make sure the Python libraries for Google's authentication library are installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/google/auth", "pip3 install google-auth")
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/google_auth_oauthlib", "pip3 install google-auth-oauthlib")

runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/googleapiclient", "pip3 install google-api-python-client")

runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/google_auth_httplib2.py", "pip3 install google-auth-httplib2")

runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/oauth2client", "pip3 install oauth2client")



# Make sure the Tomcat servlet container is installed (used for serving Guacamole client contents to users connecting to the Guacamole server via web).
runIfPathMissing("/usr/share/doc/tomcat8", "apt-get install -y tomcat8 tomcat8-admin tomcat8-common tomcat8-user")

# Make sure the Nginx web/proxy server is installed (used to proxy the Tomcat server and provide SSL)...
runIfPathMissing("/usr/share/doc/nginx", "apt-get install -y nginx")
# ...with support for Let's Encrypt. See here:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-10
# Also, see later section on crontab for monthly certbot renew / backup process.
runIfPathMissing("/usr/lib/python3/dist-packages/certbot", "apt-get install -y python3-acme python3-certbot python3-mock python3-openssl python3-pkg-resources python3-pyparsing python3-zope.interface")
runIfPathMissing("/usr/share/doc/python3-certbot-nginx", "apt-get install -y python3-certbot-nginx")
# Make sure uWSGI (WSGI component for Nginx) is installed.
runIfPathMissing("/usr/local/bin/uwsgi", "pip3 install uwsgi")
copyfile("emperor.uwsgi.service", "/etc/systemd/system/emperor.uwsgi.service", mode="0755")

# Make sure UFW is installed (Debian firewall). 
runIfPathMissing("/usr/share/doc/ufw", "apt-get install -y ufw")
# Set up firewall rules - allow HTTP and HTTPS from external IP addresses, but only allow Tomcat's port 8080 from localhost.
os.system("ufw allow OpenSSH > /dev/null 2>&1")
os.system("ufw allow http > /dev/null 2>&1")
os.system("ufw allow https > /dev/null 2>&1")
os.system("echo y | ufw enable > /dev/null 2>&1")

# Copy index.html over to the web server's live folder.
os.system("rm /var/www/html/index.nginx-debian.html > /dev/null 2>&1")
os.system("cp index.html /var/www/html")
replaceVariables("/var/www/html/index.html", {"GOOGLECLIENTID":userOptions["-googleClientID"]})

# Copy the Python API over to the appropriate uWSGI folder.
os.system("cp api.py /var/lib/nginx/uwsgi")
replaceVariables("/var/lib/nginx/uwsgi/api.py", {"GOOGLECLIENTID":userOptions["-googleClientID"],"GOOGLECLIENTSECRET":userOptions["-googleClientSecret"]})

print("Stopping Guacamole...")
os.system("systemctl stop guacd")
print("Stopping Tomcat...")
os.system("systemctl stop tomcat8")
print("Stopping Nginx...")
os.system("systemctl stop nginx")
print("Stopping uWSGI...")
os.system("systemctl stop emperor.uwsgi.service")
# Make sure Guacamole's config folders exist.
runIfPathMissing("/etc/guacamole", "mkdir /etc/guacamole")
runIfPathMissing("/etc/guacamole/extensions", "mkdir /etc/guacamole/extensions")
runIfPathMissing("/etc/guacamole/lib", "mkdir /etc/guacamole/lib")
# Build and install Guacamole.
runIfPathMissing("guacamole-server-1.0.0", "tar -xzf guacamole-server-1.0.0.tar.gz; cd guacamole-server-1.0.0; ./configure --with-init-dir=/etc/init.d; make; make install; ldconfig -v; cd ..")
# Copy accross Guacamole user mapping file.
os.system("cp user-mapping.xml /etc/guacamole")
replaceVariables("/etc/guacamole/user-mapping.xml", {"ADMINPASSWORD":userOptions["-adminPassword"], "REMOTEPASSWORD":hashlib.md5(userOptions["-remotePassword"].encode('utf-8')).hexdigest()})
# Enable the Guacamole server service.
os.system("systemctl enable guacd > /dev/null 2>&1")
# Enable the uWSGI server service.
os.system("systemctl enable emperor.uwsgi.service > /dev/null 2>&1")
# Copy over the Nginx config files.
os.system("cp nginx.conf /etc/nginx/nginx.conf")
os.system("cp default /etc/nginx/sites-available/default")
replaceVariables("/etc/nginx/sites-available/default", {"SERVERNAME":userOptions["-serverName"]})
# Copy over the Tomcat config files.
os.system("cp tomcat8 /etc/default/tomcat8")
os.system("cp server.xml /usr/share/tomcat8/skel/conf/server.xml")
# Copy over the Guacamole client (pre-compiled Java servlet)...
os.system("cp guacamole-1.0.0.war /etc/guacamole/guacamole.war")
runIfPathMissing("/var/lib/tomcat8/webapps/guacamole.war", "ln -s /etc/guacamole/guacamole.war /var/lib/tomcat8/webapps/")
print("Starting uWSGI...")
os.system("systemctl start emperor.uwsgi.service")
print("Starting Nginx...")
os.system("systemctl start nginx")
print("Starting Tomcat...")
os.system("systemctl start tomcat8")
print("Starting Guacamole server...")
os.system("systemctl start guacd")

# Set up Cron.
copyfile("crontab", "/var/spool/cron/crontabs/root", mode="0600")
os.system("dos2unix monthlyCronjob.sh > /dev/null 2>&1")
os.system("cp monthlyCronjob.sh /etc/guacamole")
os.system("chmod u+x /etc/guacamole/monthlyCronjob.sh")
os.system("/etc/init.d/cron restart")
