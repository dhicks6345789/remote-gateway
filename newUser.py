# This script is run whenever a user not listed in /etc/guacamole/user-mapping.xml logs in. If, for instance, you have your Cloudflare Zero Trust application
# set up to allow all users in your domain to log in but you don't want to have to pre-create accounts for every user onyour domain, you can have this script
# create accounts as needed. Uncomment the section you want to use.



# Use SSH (athorised with a private key) to create a new user on a Windows server.
import sys
import logging

# Get parameters passed from the CGI script.
username = sys.argv[1]
password = sys.argv[2]
# Set up logging.
logging.basicConfig(filename="/var/log/remote-gateway/remote-gateway.log", encoding="utf-8", format="%(asctime)s - %(message)s", level=logging.INFO)
# Run the "create user" command remotely via SSH on the Windows server. You'll need to set up SSH Server on your Windows server (now included as a standard
# component of Windows) and set up a private key for authorisation. Replace the IP address in the line below with the address / name of your server.
os.system("ssh -i /root/.ssh/id_rsa administrator@192.168.1.112 -t \"net user " + username + " " + password " /add\"")
# Log what we've done.
logging.info("Added new user: " + username)
# Return the new username and password to the calling CGI script.
print(username + "," + password)



## Default behaviour - do nothing, return an empty string.
# print("")
