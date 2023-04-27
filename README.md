# remote-gateway

A script to configure a Debian installation as a remote desktop gateway, using Apache Guacamole to provide web-based remote desktop and Cloudflare's Zero Trust product for handling authentication and security.

## What Does This Script Do
This script is intended for people who want to set up a remote desktop gateway server with authentication and security (HTTPS, DDoS protection, etc) handled by Cloudflare. If you're using this script it's assumed you are probably a system administrator of some sort wanting to set up a remote desktop gateway for your users.

All the software installed by this script is free and open source, and (at the time of writing, April 2023) Cloudflare's Zero Trust product is free for up to 50 users of a domain, so it is suitible for home users and smaller businesses. If you have over 50 users then Cloudflare's system is still an excellent choice, you'll just need to start paying for usage.

The installation procedure below is intended to run on a server of some kind - either a physical server or, most probably these days, a virtual machine running as part of a company's internal server complement. It should also work for servers running on remote infrastructure, in a datacentre somewhere.

Don't run the install script on your desktop machine, or any machine that you can't simply re-install or restore to a previous checkpoint. This script shouldn't actually do anything destructive, and it should mostly work alongside other applications installed on a server, but to avoid issues it is recommended that you dedicate a machine or VM to this. This script, if it works correctly, should result in your machine running instances of nginx, uWSGI, Tomcat and Guacamole. It is also recommended that the target remote desktop server be a separate machine (or VM).

## Before You Start
The setup this script results in relies on Cloudflare's tunneling client being present. It assumes all network traffic comes through that tunnel. You will need a Cloudflare account (the free option is fine) and will need to define a Cloudflare tunnel and (self hosted) Zero Trust application on their control panel. To accomplish both of those things you will need to have control of the domain you are using and for that domain to be using Cloudflare's DNS servers.

## Installation

Download from Github and run the install script:
```
git clone https://github.com/dhicks6345789/remote-gateway.git --no-rebase
bash remote-gateway/install.sh -servername guacamole.your.domain -databasepw SomePassword -guacpw SomePassword
```
You'll need to provide three values: the name of the server (should be your server's domain name)

## Notes
Not finished yet - not ready for real-world use. Especially don't use on a Debian install you need for anything else.
