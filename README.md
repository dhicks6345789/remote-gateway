# remote-gateway

A script to configure a Debian installation as a remote desktop gateway, using Apache Guacamole to provide web-based remote desktop and Cloudflare's [Zero Trust product](https://www.cloudflare.com/en-gb/products/zero-trust/) for handling authentication and security.

## What Does This Project Do?
This project provides a setup script that is intended for people who want to set up a remote desktop gateway server with authentication and security (HTTPS, DDoS protection, etc) handled by Cloudflare. If you're using this project it's assumed you are probably a system administrator of some sort wanting to set up a remote desktop gateway for your users.

If you found this project but just wanted a script to help you install Guacamole without using Cloudflare, then you probably want the [Guac Install](https://github.com/MysticRyuujin/guac-install) project. This project currently builds on that project, although at some point it will probably use a different [Guacamole Setup](https://github.com/itiligent/Guacamole-Setup) project.

All the software installed by this projct is free and open source, and (at the time of writing, April 2023) Cloudflare's Zero Trust product is free for up to 50 users of a domain, so it is suitible for home users and smaller businesses. If you have over 50 users then Cloudflare's system is still an excellent choice, you'll just need to start paying for usage.

The installation procedure below is intended to run on a server of some kind - either a physical server or, most probably these days, a virtual machine running as part of a company's internal server complement. It should also work for servers running on remote infrastructure, in a datacentre somewhere.

Don't run the install script on your desktop machine, or any machine that you can't simply re-install or restore to a previous checkpoint. The setup script shouldn't actually do anything destructive, and it should mostly work alongside other applications installed on a server, but to avoid issues it is recommended that you dedicate a machine or VM to this. The setup script, if it works correctly, should result in your machine running instances of [NGINX](https://www.nginx.com/), [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/), Apache [Tomcat](https://tomcat.apache.org/) and Apache [Guacamole](https://guacamole.apache.org/). It is also recommended that the target remote desktop server be a separate machine (or VM).

## Before You Start
The setup this script results in relies on Cloudflare's tunneling client ([cloudflared](https://github.com/cloudflare/cloudflared) - link included for completeness, but you probably just want to download a binary to install from Cloudflare's admin console) being present. It assumes all network traffic comes through that tunnel. You will need a Cloudflare account (the free option is fine) and will need to define a Cloudflare tunnel and (self hosted) Zero Trust application on their control panel. To accomplish both of those things you will need to have control of the domain you are using and for that domain to be using Cloudflare's DNS servers. You will want to pick a subdomain to host the Zero Trust application (e.g. "guacamole.yourdomain.com").

Cloudflare's Zero Trust product allows you to authenticate users via various means, including via OAuth for several providers. This is a way to offer users web-based remote desktop access to a Windows desktop, seemlessly authenticated by their coprorate (or education) Google / Microsoft / etc accounts. You'll need to follow Cloudflare's instructions to add the authentication methods you want your users to use to the Zero Trust applications you define - you'll probably need to be the administrator of your organisations Google Workspace / Microsoft 365 Instance / etc.

You will need a machine / VM running Debian. You probably want a newly-installed, dedicated machine / VM created just for this purpose. Debian can be installed with SSH access only, without a graphical desktop, if you want, no part of this project or Guacamole need you to have a graphical interface.

You will also want a target remote desktop server of some sort. This should probably be a separate machine / VM from the one you're using as a gateway, although you could put everything on one. You can have multiple target machines if you want, and Guacamole supports SSH, VNC and RDP, so your targets can be Linux, Mac or Windows.

## Installation

Download from Github and run the install script:
```
git clone https://github.com/dhicks6345789/remote-gateway.git
bash remote-gateway/install.sh -servername guacamole.yourdomain.com -databasepw SomePassword -guacpw SomePassword
```
You'll need to provide three values:
- The full domain name of the server (should be your server's domain name, where the Cloudflare DNS entry / Zero Trust application is pointing, e.g. "guacamole.yourdomain.com")
- A password for the MySQL database that will be created by the Guacamole install script.
- An admin password for Guacamole itself.

The script will take a little while to run - it downloads and installs various components as it goes along, it might take half an hour or so.

## After Installation

When finished, you should (hopefully) have a Debian server running:
- uswgi

## Notes
Not finished yet - might still be a bit clunky in places, but should mostly work.

### To do:
- Possibly add support for services similar to Cloudflare's Zero Trust - ngrok, maybe.
- Make script runnable via direct download rather than having to clone project.
