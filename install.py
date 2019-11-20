#!/usr/bin/python3

import os
import sys
import shutil

# Parse any options set by the user on the command line.
validBooleanOptions = []
validValueOptions = ["-googleKey"]
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

# Set up the Debian sources.list file - we need to use a library not included in the current Debian release.
copyfile("sources.list", "/etc/apt/sources.list", mode="0644")

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
runIfPathMissing("/usr/share/doc/libfreerdp2-dev", "apt-get install -y libfreerdp2-dev")

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

# Make sure the Tomcat servlet container is installed (used for serving Guacamole client contents to users connecting to the Guacamole server via web).
runIfPathMissing("/usr/share/doc/tomcat9", "apt-get install -y tomcat9 tomcat9-admin tomcat9-common tomcat9-user")

# Make sure the Nginx web/proxy server is installed (used to proxy the Tomcat server and provide SSL)...
runIfPathMissing("/usr/share/doc/nginx", "apt-get install -y nginx")
# ...with support for Let's Encrypt. See here:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-9
# Also, see later section on crontab for daily certbot renew / backup process.
#runIfPathMissing("/usr/lib/python3/dist-packages/certbot", "apt-get install -y python-certbot-nginx -t stretch-backports")

# Make sure UFW is installed (Debian firewall). 
runIfPathMissing("/usr/share/doc/ufw", "apt-get install -y ufw")
# Set up firewall rules - allow HTTP and HTTPS from external IP addresses, but only allow Tomcat's port 8080 from localhost.
os.system("ufw allow OpenSSH > /dev/null 2>&1")
os.system("ufw allow http > /dev/null 2>&1")
os.system("ufw allow https > /dev/null 2>&1")
os.system("echo y | ufw enable > /dev/null 2>&1")

print("Stopping Guacamole...")
os.system("systemctl stop guacd")
print("Stopping Tomcat...")
os.system("systemctl stop tomcat9")
print("Stopping Nginx...")
os.system("systemctl stop nginx")
# Make sure Guacamole's config folders exist.
runIfPathMissing("/etc/guacamole", "mkdir /etc/guacamole")
runIfPathMissing("/etc/guacamole/extensions", "mkdir /etc/guacamole/extensions")
runIfPathMissing("/etc/guacamole/lib", "mkdir /etc/guacamole/lib")
# Build and install Guacamole.
runIfPathMissing("guacamole-server-1.0.0", "tar -xzf guacamole-server-1.0.0.tar.gz; cd guacamole-server-1.0.0; ./configure --with-init-dir=/etc/init.d; make; make install; ldconfig -v; cd ..")
# Copy accross Guacamole user mapping file.
os.system("cp user-mapping.xml /etc/guacamole")
# Enable the Guacamole server service.
os.system("systemctl enable guacd > /dev/null 2>&1")
# Copy over the Nginx config files.
os.system("cp nginx.conf /etc/nginx/nginx.conf")
os.system("cp default /etc/nginx/sites-available/default")
# Copy over the Tomcat config files.
os.system("cp tomcat9 /etc/default/tomcat9")
os.system("cp server.xml /usr/share/tomcat9/skel/conf/server.xml")
# Copy over the Guacamole client (pre-compiled Java servlet)...
os.system("cp guacamole-1.0.0.war /etc/guacamole/guacamole.war")
runIfPathMissing("/var/lib/tomcat9/webapps/guacamole.war", "ln -s /etc/guacamole/guacamole.war /var/lib/tomcat9/webapps/")
print("Starting Nginx...")
os.system("systemctl start nginx")
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
