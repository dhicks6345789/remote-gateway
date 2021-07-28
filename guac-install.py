#!/usr/bin/python3

import os
import sys
#import shutil
#import hashlib
#import random

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

# First, get some needed values from the user, if they haven't already provided them on the command line.
print("Installing...")
getUserOption("-serverName", "Please enter this server's full name (e.g. server.domain.com)")
getUserOption("-databasePassword", "Please enter the password to set for Guacamole's database")
getUserOption("-guacPassword", "Please enter the password to set for Guacamole")
    
os.system("wget https://git.io/fxZq5 -O guac-install.sh")
os.system("chmod +x guac-install.sh")
os.system("cd /; ./guac-install.sh --mysqlpwd " + userOptions["-databasePassword"] + " --guacpwd " + userOptions["-guacPassword"] + " --nomfa --installmysql")
