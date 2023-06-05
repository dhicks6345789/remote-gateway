copyOrDownload () {
    echo Copying $1 to $2, mode $3...
    if [ -f $1 ]; then
        cp $1 $2
    elif [ -f remote-gateway/$1 ]; then
        cp remote-gateway/$1 $2
    else
        wget https://github.com/dhicks6345789/remote-gateway/raw/master/$1 -O $2
    fi
    chmod $3 $2
}

pagetitle="Guacamole"
# Read user-defined command-line flags.
while test $# -gt 0; do
    case "$1" in
        -servername)
            shift
            servername=$1
            shift
            ;;
        -databasepw)
            shift
            databasepw=$1
            shift
            ;;
        -guacpw)
            shift
            guacpw=$1
            shift
            ;;
        -pagetitle)
            shift
            pagetitle=$1
            shift
            ;;
        *)
            echo "$1 is not a recognized flag!"
            exit 1;
            ;;
    esac
done

# Check all required flags are set, print a usage message if not.
if [ -z "$servername" ] || [ -z "$databasepw" ] || [ -z "$guacpw" ]; then
    echo "Usage: install.sh -servername SERVERNAME -databasepw DATABASEPASSWORD -guacpw GACAMOLEPASSWORD [-pagetitle PAGETITLE]"
    echo "SERVERNAME: The full domain name of the Guacamole server (e.g. guacamole.example.com)"
    echo "DATABASEPASSWORD: The password to set for Guacamole's database."
    echo "GUACAMOLEPASSWORD: The password to set for Guacamole itself."
    echo "Optional: PAGETITLE: A title for the HTML page (tab title) displayed."
    exit 1;
fi

# Use Chase Wright's script to install a Guacamole server - see: https://github.com/MysticRyuujin/guac-install
if [ ! -d "/etc/guacamole" ]; then
    wget https://git.io/fxZq5 -O guac-install.sh
    chmod +x guac-install.sh
    ./guac-install.sh --mysqlpwd " + $databasepw + " --guacpwd " + $guacpw + " --nomfa --installmysql
    rm guac-install.sh
fi
# Todo: above script is now (April 2023) out of date, switch to a newer one. For now:
if [ -f "/etc/guacamole/extensions/guacamole-auth-jdbc-mysql-1.5.0.jar" ]; then
    rm /etc/guacamole/extensions/guacamole-auth-jdbc-mysql-1.5.0.jar
fi



# Make sure the Nginx web/proxy server is installed (used to proxy the Tomcat server and provide SSL).
if [ ! -d "/etc/nginx" ]; then
    apt install -y nginx
fi

# Figure out what version of Python3 we have installed.
pythonVersion=`ls /usr/local/lib | grep python3`

# Make sure Pip (Python package manager) is installed.
if [ ! -f "/usr/bin/pip3" ]; then
    apt install -y python3-pip
fi

# Make sure uWSGI (WSGI component for Nginx) is installed...
if [ ! -f "/usr/local/bin/uwsgi" ]; then
    pip3 install uwsgi
fi

# Make sure Flask (Python web-publishing framework, used for the Python CGI script) is installed.
if [ ! -d "/usr/local/lib/$pythonVersion/dist-packages/flask" ]; then
    pip3 install flask
fi



# Make sure the remote-gateway folder and files exist.
if [ ! -d "/etc/remote-gateway" ]; then
    mkdir /etc/remote-gateway
fi

if [ ! -f "/etc/remote-gateway/newUser.xml" ]; then
    copyOrDownload newUser.xml /etc/remote-gateway/newUser.xml 0755
fi

if [ ! -f "/etc/remote-gateway/newUser.py" ]; then
    copyOrDownload newUser.py /etc/remote-gateway/newUser.py 0755
fi

# Make sure a folder with the correct permissions exists for remote-gateway to write log files.
if [ ! -d "/var/log/remote-gateway" ]; then
    mkdir /var/log/remote-gateway
    chown www-data:www-data /var/log/remote-gateway
fi

if [ ! -d "/var/www/.ssh" ]; then
    mkdir /var/www/.ssh
    chown www-data:www-data /var/www/.ssh
    chmod 700 /var/www/.ssh
fi



echo "Stopping Guacamole..."
systemctl stop guacd

echo "Stopping Tomcat..."
systemctl stop tomcat9

echo "Stopping uWSGI..."
systemctl stop emperor.uwsgi.service

echo "Stopping Nginx..."
systemctl stop nginx

# Make sure the Guacamole user-mapping file exists - download our example file if there's no file there already.
if [ ! -f /etc/guacamole/user-mapping.xml ]; then
    copyOrDownload user-mapping.xml /etc/guacamole/user-mapping.xml 0755
fi
chown www-data /etc/guacamole/user-mapping.xml

if [ -f /etc/remote-gateway/id_rsa ]; then
    chown www-data:www-data /etc/remote-gateway/id_rsa
fi



# Copy over the WSGI configuration and code.
copyOrDownload emperor.uwsgi.service /etc/systemd/system/emperor.uwsgi.service 0755
systemctl daemon-reload
copyOrDownload api.py /var/lib/nginx/uwsgi/api.py 0755
sed -i "s/Guacamole/$pagetitle/g" /var/lib/nginx/uwsgi/api.py
copyOrDownload client.html /var/www/html/client.html 0755
copyOrDownload error.html /var/www/html/error.html 0755
copyOrDownload registerPi.sh /var/www/html/registerPi.sh 0755

if [ ! -d /var/www/html/favicon ]; then
    mkdir /var/www/html/favicon
    copyOrDownload favicon/android-chrome-192x192.png /var/www/html/favicon/android-chrome-192x192.png 0755
    copyOrDownload favicon/android-chrome-512x512.png /var/www/html/favicon/android-chrome-512x512.png 0755
    copyOrDownload favicon/apple-touch-icon.png /var/www/html/favicon/apple-touch-icon.png 0755
    copyOrDownload favicon/browserconfig.xml /var/www/html/favicon/browserconfig.xml 0755
    copyOrDownload favicon/favicon-16x16.png /var/www/html/favicon/favicon-16x16.png 0755
    copyOrDownload favicon/favicon-32x32.png /var/www/html/favicon/favicon-32x32.png 0755
    copyOrDownload favicon/favicon.ico /var/www/html/favicon/favicon.ico 0755
    copyOrDownload favicon/mstile-144x144.png /var/www/html/favicon/mstile-144x144.png 0755
    copyOrDownload favicon/mstile-150x150.png /var/www/html/favicon/mstile-150x150.png 0755
    copyOrDownload favicon/mstile-310x150.png /var/www/html/favicon/mstile-310x150.png 0755
    copyOrDownload favicon/mstile-310x310.png /var/www/html/favicon/mstile-310x310.png 0755
    copyOrDownload favicon/mstile-70x70.png /var/www/html/favicon/mstile-70x70.png 0755
    copyOrDownload favicon/safari-pinned-tab.svg /var/www/html/favicon/safari-pinned-tab.svg 0755
    copyOrDownload favicon/site.webmanifest /var/www/html/favicon/site.webmanifest 0755
fi

# Enable the uWSGI server service.
systemctl enable emperor.uwsgi.service

# Copy over the Nginx config files.
copyOrDownload nginx.conf /etc/nginx/nginx.conf 0644
copyOrDownload default /etc/nginx/sites-available/default 0644
sed -i "s/SERVERNAME/$servername/g" /etc/nginx/sites-available/default



echo "Starting Nginx..."
systemctl start nginx

echo "Starting uWSGI..."
systemctl start emperor.uwsgi.service

echo "Starting Tomcat..."
systemctl start tomcat9

echo "Starting Guacamole server..."
systemctl start guacd
