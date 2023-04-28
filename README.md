# remote-gateway

A script to configure a Debian installation as a remote desktop gateway, using Apache Guacamole to provide web-based remote desktop and Cloudflare's [Zero Trust product](https://www.cloudflare.com/en-gb/products/zero-trust/) for handling authentication and security.

## What Does This Project Do?
This project provides a setup script that is intended for people who want to set up a remote desktop gateway server with authentication and security (HTTPS, DDoS protection, etc) handled by Cloudflare. If you're using this project it's assumed you are probably a system administrator of some sort wanting to set up a remote desktop gateway for your users.

If you found this project but just wanted a script to help you install a standard instance of Guacamole, without using Cloudflare, then you probably want the [Guac Install](https://github.com/MysticRyuujin/guac-install) project. This project currently builds on that project, although at some point it will probably use a different [Guacamole Setup](https://github.com/itiligent/Guacamole-Setup) project.

All the software installed by this project is free and open source, and (at the time of writing, April 2023) Cloudflare's Zero Trust product is free for up to 50 users of a domain, so it is suitible for home users and smaller businesses. If you have over 50 users then Cloudflare's system is still an excellent choice, you'll just need to start paying for usage.

The installation procedure below is intended to run on a server of some kind - either a physical server or, most probably these days, a virtual machine running as part of a company's internal server complement. It should also work for servers running on remote infrastructure, in a datacentre somewhere.

Don't run the install script on your desktop machine, or any machine that you can't simply re-install or restore to a previous checkpoint. The setup script shouldn't actually do anything destructive, and it should mostly work alongside other applications installed on a server, but to avoid issues it is recommended that you dedicate a machine or VM to this. The setup script, if it works correctly, should result in your machine running instances of [NGINX](https://www.nginx.com/), [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/), Apache [Tomcat](https://tomcat.apache.org/) and Apache [Guacamole](https://guacamole.apache.org/). It is also recommended that the target remote desktop server be a separate machine (or VM).

## Before You Start
The setup this script results in relies on Cloudflare's tunneling client ([cloudflared](https://github.com/cloudflare/cloudflared) - link to source code on Github included for completeness, but you probably just want to download a ready-to-go binary to install from Cloudflare's admin console) being present. It assumes all network traffic comes through that tunnel. You will need a Cloudflare account (the free option is fine) and will need to define a Cloudflare tunnel and (self hosted) Zero Trust application on their control panel. To accomplish both of those things you will need to have control of the domain you are using and for that domain to be using Cloudflare's DNS servers. You will want to pick a subdomain to host the Zero Trust application (e.g. "guacamole.yourdomain.com").

Cloudflare's Zero Trust product allows you to authenticate users via various means, including via OAuth for several providers. This is a good way to offer users web-based remote desktop access to a Windows desktop, seemlessly authenticated by their coprorate (or education) Google / Microsoft / etc accounts. You'll need to follow Cloudflare's instructions to add the authentication methods you want your users to use to the Zero Trust applications you define - you'll probably need to be the administrator of your organisations Google Workspace / Microsoft 365 Instance / etc.

You will need a machine / VM running Debian. You probably want a newly-installed, dedicated machine / VM created just for this purpose. Debian can be installed with SSH access only, without a graphical desktop, if you want, no part of this project or Guacamole need you to have a graphical interface.

You will also want a target remote desktop server of some sort. This should probably be a separate machine / VM from the one you're using as a gateway, although you could put everything on one. You can have multiple target machines if you want, and Guacamole supports SSH, VNC and RDP, so your targets can be Linux, Mac or Windows.

Handling setup and licensing for a Windows remote desktop server is beyond the scope of this project. If you want to use a Windows remote desktop, you will need to check you have the appropriate CALs / remote connector licensing in place for your organisation. If you are trying to get an older, legacy Windows application to be able to be run via a web browser but Windows remote desktop licesning is going to be too costly or complex, the [Wine](https://www.winehq.org/) project, which can allow you to run some Windows applications on Linux or similar, might be of use.

## Installation
On a freshly installed Debian server, as root, run the command:
```
wget https://github.com/dhicks6345789/remote-gateway/raw/master/install.sh -q -O - | bash -s -- -servername guacamole.yourdomain.com -databasepw SomePassword01 -guacpw SomePassword02
```
Or, download from Github and run the install script:
```
git clone https://github.com/dhicks6345789/remote-gateway.git
bash remote-gateway/install.sh -servername guacamole.yourdomain.com -databasepw SomePassword01 -guacpw SomePassword02
```
You'll need to provide three values:
- The full domain name of the server (should be your server's domain name, where the Cloudflare DNS entry / Zero Trust application is pointing, e.g. "guacamole.yourdomain.com")
- A password for the MySQL database that will be created by the Guacamole install script.
- An admin password for Guacamole itself.

The script will take a little while to run - it downloads and installs various components as it goes along, it might take half an hour or so.

## After Installation

When the above script has finished, you should (hopefully) have a Debian server running:
 - Guacamole, hosted as an application inside Tomcat, listening (via HTTP only, not HTTPS) on port 8080, i.e. http://localhost:8080/guacamole
 - NGINX, listening (again via HTTP only) on (HTTP standard) port 80, as a reverse proxy to both Guacamole (http://localhost/guacamole) and uWSGI (http://localhost/) running our own simple Python CGI (using the [Flask](https://flask.palletsprojects.com) framework) script.

You will then need to install the Cloudflare tunnel client (cloudflared). Follow Cloudflare's instructions given from their control panel, it's simple enough.

In the setup for the Cloudflare tunnel, when asked for a Public Hostname for the tunnel, you'll want to select "HTTP" and "localhost:80".

The Cloudflare tunnel will take care of handling HTTPS traffic, complete with automatic handling / refresh of certificates, to ensure your connection is secure. Authentication is also handled by Cloudflare, with the authenticated user's details being passed in via the header from the tunnel client to the NGINX server. The CGI script picks up those details to create an HTML page for each user that logs in that passes login details through to Guacamole.

If you want to change the page title from the default "Guacamole", simply edit the file "/var/lib/nginx/uwsgi/api.py" and replace the string on the line that starts "pageTitle =" with your preferred title.

### Adding Connections / Users

The CGI script that picks up the authenticated username provided by cloudflared reads Guacamole's user-mapping.xml file (/etc/guacamole/user-mapping.xml) to try and find any matching users listed. Authenticated users' usernames will generally be in the form of an email address, the domain part is removed by the CGI script. So, a user logging in with the email address "f.bloggs@example.com" will be seen as user "f.bloggs" in user-mapping.xml.

An example user-mapping.xml file is provided to get you started. You can read Guacmaole's own [documentation](https://guacamole.apache.org/doc/gug/configuring-guacamole.html) for more details.

The CGI script will simply pass any connection password for a found user out to the page that displays the remote desktop interface. This page hides the URL (which includes the username and password) by using a 100% height and width iframe element.

## Notes
This script is, hopefully, mostly complete and has been tested with a couple of real-life installations. There might still be issues in places, do please report any issues you find.

### To do:
- Add ability to add new users to Windows machines as new users log in.
- Add support for favicon / custom window title.
- Rewrite crontab to auto-update?
- Possibly add support for services similar to Cloudflare's Zero Trust - ngrok, maybe.
- Add support for classroom sets of Raspberry Pis, with user interface for admin user(s) to edit list of devices available.
- Add support for legacy Windows apps, with file save/load.
