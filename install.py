#!/usr/bin/python3

import os
import sys
#import time
import shutil
#import hashlib

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

# Make sure Flask (Python web-publishing framework) is installed.
#runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/flask", "pip3 install flask")

# Make sure Expect (command-line automation utility) is installed.
#runIfPathMissing("/usr/bin/expect", "apt-get -y install expect")

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

# Make sure the Tomcat servlet container is installed (used for serving Guacamole client contents to users connecting to the Guacamole server via web).
runIfPathMissing("/usr/share/doc/tomcat8", "apt-get install -y tomcat8 tomcat8-admin tomcat8-common tomcat8-user")

# Make sure the Nginx web/proxy server is installed (used to proxy the Tomcat server and provide SSL)...
runIfPathMissing("/usr/share/doc/nginx", "apt-get install -y nginx")
# ...with support for Let's Encrypt. See here:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-9
# Also, see later section on crontab for daily certbot renew / backup process.
#runIfPathMissing("/usr/lib/python3/dist-packages/certbot", "apt-get install -y python-certbot-nginx -t stretch-backports")

sys.exit(0)

# Make sure Apache (web server) is installed...
#runIfPathMissing("/etc/apache2", "apt-get install -y apache2")
# ...with SSL enabled...
#os.system("a2enmod ssl > /dev/null")
# ...and mod_rewrite...
#os.system("a2enmod rewrite > /dev/null")
# ...along with mod_wsgi...
#runIfPathMissing("/usr/share/doc/libapache2-mod-wsgi-py3", "apt-get install -y libapache2-mod-wsgi-py3 python-dev")
#os.system("a2enmod wsgi > /dev/null")
# ...and Certbot, for Let's Encrypt SSL certificates.
#runIfPathMissing("/usr/lib/python3/dist-packages/certbot", "apt-get install -y certbot python-certbot-apache")

#getUserOption("-domainName", "Please enter this site's domain name")

# If this project already includes a Let's Encrypt certificate, install that. Otherwise, ask the user if we should set one up.
# Code goes here - check if there's an archived SSL cedtiftcate to unpack.
print("Set up Let's Encrypt certificate?")
print("This server needs to have a valid DNS entry pointing at it first - select \"no\" and you'll get a non-SSL server for testing, re-run this script with the \"-redoApacheConfig\" option to change.")
userSelection = askUserMenu(["Yes - single domain name.","Yes - wildcard domain.","No"])
# Stop Apache while we update the config.
os.system("apachectl stop")
# Pause for a moment to make sure apache has actually stopped.
time.sleep(4)
if userSelection == 1:
    print("Code goes here...")
    #os.system("certbot")
elif userSelection == 2:
    print("Code goes here...")
elif userSelection == 3:
    # Copy over the Apache configuration file.
    copyfile("000-default-without-SSL.conf", "/etc/apache2/sites-available/000-default.conf", mode="0744")
replaceVariables("/etc/apache2/sites-available/000-default.conf", {"DOMAINNAME":userOptions["-domainName"]})
# Copy over the WSGI configuration file.
copyfile("api.wsgi", "/var/www/api.wsgi", mode="0744")
# Copy over the API.
os.makedirs("/var/www/api", exist_ok=True)
copyfile("api.py", "/var/www/api/api.py", mode="0744")
copyfile("build.html", "/var/www/api/build.html", mode="744")
# Start Apache back up again.
os.system("apachectl start")

# Make sure Rclone is set up to connect to the user's cloud storage - we might need to ask the user for some details.
if not os.path.exists("/root/.config/rclone/rclone.conf"):
    print("Configuring rclone...")
    getUserOption("-contentFolderPath", "Please enter the path that contains the content")
    getUserOption("-jekyllFolderPath", "Please enter the path that contains the Jekyll setup")
    runExpect([
        "spawn /usr/bin/rclone config",
        "expect \"n/s/q>\"",
        "send \"n\\r\"",
        "expect \"name>\"",
        "send \"drive\\r\"",
        "expect \"Storage>\"",
        "send \"drive\\r\"",
        "expect \"client_id>\"",
        "expect_user -timeout 3600 -re \"(.*)\\n\"",
        "send \"$expect_out(1,string)\\r\"",
        "expect \"client_secret>\"",
        "expect_user -timeout 3600 -re \"(.*)\\n\"",
        "send \"$expect_out(1,string)\\r\"",
        "expect \"scope>\"",
        "send \"drive.readonly\\r\"",
        "expect \"root_folder_id>\"",
        "send \"\\r\"",
        "expect \"service_account_file>\"",
        "send \"\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"Enter verification code>\"",
        "expect_user -timeout 3600 -re \"(.*)\\n\"",
        "send \"$expect_out(1,string)\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/e/d>\"",
        "send \"y\\r\"",
      
        "expect \"e/n/d/r/c/s/q>\"",
        "send \"n\\r\"",
        "expect \"name>\"",
        "send \"content\\r\"",
        "expect \"Storage>\"",
        "send \"cache\\r\"",
        "expect \"remote>\"",
        "send \"drive:"+userOptions["-contentFolderPath"]+"\\r\"",
        "expect \"plex_url>\"",
        "send \"\\r\"",
        "expect \"plex_username>\"",
        "send \"\\r\"",
        "expect \"y/g/n>\"",
        "send \"n\\r\"",
        "expect \"chunk_size>\"",
        "send \"10M\\r\"",
        "expect \"info_age>\"",
        "send \"1y\\r\"",
        "expect \"chunk_total_size>\"",
        "send \"1G\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/e/d>\"",
        "send \"y\\r\"",
        
        
        "expect \"e/n/d/r/c/s/q>\"",
        "send \"n\\r\"",
        "expect \"name>\"",
        "send \"jekyll\\r\"",
        "expect \"Storage>\"",
        "send \"cache\\r\"",
        "expect \"remote>\"",
        "send \"drive:"+userOptions["-jekyllFolderPath"]+"\\r\"",
        "expect \"plex_url>\"",
        "send \"\\r\"",
        "expect \"plex_username>\"",
        "send \"\\r\"",
        "expect \"y/g/n>\"",
        "send \"n\\r\"",
        "expect \"chunk_size>\"",
        "send \"10M\\r\"",
        "expect \"info_age>\"",
        "send \"1y\\r\"",
        "expect \"chunk_total_size>\"",
        "send \"1G\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/e/d>\"",
        "send \"y\\r\"",
        
        "send \"q\\r\""
    ])

# Set up rclone to mount the user's cloud storage - first, stop any existing rclone mount process...
os.system("systemctl stop rclone-content")
os.system("systemctl stop rclone-jekyll")
# ...make sure FUSE is configured to allow non-root users to access mounts...
copyfile("fuse.conf", "/etc/fuse.conf", mode="644")
# ...make sure the mount point and cache folders exist...
os.makedirs("/mnt/content", exist_ok=True)
os.makedirs("/mnt/jekyll", exist_ok=True)
os.makedirs("/var/cache/rclone-content", exist_ok=True)
os.makedirs("/var/cache/rclone-jekyll", exist_ok=True)
# ...then set up systemd to mount the repository.
copyfile("rclone-content.service", "/etc/systemd/system/rclone-content.service", mode="644")
copyfile("rclone-jekyll.service", "/etc/systemd/system/rclone-jekyll.service", mode="644")
os.system("systemctl start rclone-content")
os.system("systemctl start rclone-jekyll")
os.system("systemctl enable rclone-content")
os.system("systemctl enable rclone-jekyll")

# Copy accross the build.sh script.
copyfile("build.sh", "/usr/local/bin/build.sh", mode="755")

# Copy over the Python scipt that cleans up HTML files.
copyfile("tidyHTML.py", "/usr/local/bin/tidyHTML.py", mode="0755")
os.system("chown www-data:www-data /usr/local/bin/tidyHTML.py")

# Install DocsToMarkdown.
runIfPathMissing("/usr/local/bin/docsToMarkdown.py", "curl https://raw.githubusercontent.com/dhicks6345789/docs-to-markdown/master/docsToMarkdown.py -o /usr/local/bin/docsToMarkdown.py; chmod a+x /usr/local/bin/docsToMarkdown.py; echo > /var/log/build.log; chown www-data:www-data /var/log/build.log")
runIfPathMissing("/var/local/jekyll", "mkdir /var/local/jekyll; chown www-data:www-data /var/local/jekyll")
copyfile("docsToMarkdown.json", "/var/local/docsToMarkdown.json", mode="644")
os.system("chown www-data:www-data /var/local/docsToMarkdown.json")

# Make sure we have a (hashed) build password stored.
if not os.path.exists("/var/local/buildPassword.txt"):
    getUserOption("-buildPassword", "Enter a password to use for site rebuilds")
    correctPasswordHash = hashlib.sha256(userOptions["-buildPassword"].encode("utf-8")).hexdigest()
    writeFile("/var/local/buildPassword.txt", correctPasswordHash)
    os.system("chown www-data:www-data /var/local/buildPassword.txt")
    
