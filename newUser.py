# This script is run whenever a user not listed in /etc/guacamole/user-mapping.xml logs in. If, for instance, you have your Cloudflare Zero Trust application
# set up to allow all users in your domain to log in but you don't want to have to pre-create accounts for every user onyour domain, you can have this script
# create accounts as needed. Uncomment the section you want to use.

import os
import sys
import logging
import subprocess

# Get parameters passed from the CGI script.
username = sys.argv[1]
password = sys.argv[2]

# Set up logging.
logging.basicConfig(filename="/var/log/remote-gateway/remote-gateway.log", encoding="utf-8", format="%(asctime)s - %(message)s", level=logging.INFO)

# Run the given command, with the given parameters, capture and log the result.
def runAndLog(theParameters):
  logging.info("Running: " + " ".join(theParameters))
  commandProcess = subprocess.run(theParameters, stdout=subprocess.PIPE)
  for resultLine in commandProcess.stdout.decode("utf-8").split("\n"):
    if resultLine.strip() != "":
      logging.info("   " + resultLine.strip())



## Default behaviour - log the login attempt, return a blank value.
#logging.info("User denined access: " + username)
#print("")



# Run the "create user" command remotely via SSH on a Windows server. You'll need to set up SSH Server on your Windows server (now included as a standard
# component of Windows) and set up a private key for authorisation. Replace the IP address in the line below with the address / name of your server.
runAndLog(["/usr/bin/ssh", "-i", "/var/www/id_rsa", "-o", "StrictHostKeyChecking=no", "administrator@192.168.1.112", "-t", "\"net user " + username + " " + password + " /ADD /Y 2>&1\"", "2>&1"])
#runAndLog("ssh", "-i /var/www/id_rsa administrator@192.168.1.112 -t \"net localgroup 'Remote Desktop Users' " + username + " /add 2>&1\" 2>&1")
# Return the new username and password to the calling CGI script.
print(username + "," + password)
