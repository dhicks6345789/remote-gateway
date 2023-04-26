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
        *)
            echo "$1 is not a recognized flag!"
            exit 1;
            ;;
    esac
done

# Check all required flags are set, print a usage message if not.
if [ -z "$servername" ] || [ -z "$databasepw" ] || [ -z "$guacpw" ]; then
    echo "Usage: install.sh -servername SERVERNAME -databasepw DATABASEPASSWORD -guacpw GACAMOLEPASSWORD"
    echo "SERVERNAME: The full domain name of the Guacamole server (e.g. guacamole.example.com)"
    echo "DATABASEPASSWORD: The password to set for Guacamole's database."
    echo "GUACAMOLEPASSWORD: The password to set for Guacamole itself."
    exit 1;
fi

# Use Chase Wright's script to install a Guacamole server - see: https://github.com/MysticRyuujin/guac-install
if [ ! -f "guac-install.sh" ]; then
    wget https://git.io/fxZq5 -O guac-install.sh
    chmod +x guac-install.sh
    ./guac-install.sh --mysqlpwd " + $databasepw + " --guacpwd " + $guacpw + " --nomfa --installmysql
fi
# Todo: above script is now (April 2023) out of date, switch to a newer one. For now:
if [ -f "/etc/guacamole/extensions/guacamole-auth-jdbc-mysql-1.5.0.jar" ]; then
    rm /etc/guacamole/extensions/guacamole-auth-jdbc-mysql-1.5.0.jar
fi



# Make sure the Nginx web/proxy server is installed (used to proxy the Tomcat server and provide SSL).
if [ ! -d "/etc/nginx" ]; then
    apt install -y nginx
fi

# Make sure Pip (Python package manager) is installed.
if [ ! -f "/usr/bin/pip3" ]; then
    apt install -y python3-pip
fi

# Make sure uWSGI (WSGI component for Nginx) is installed...
if [ ! -f "/usr/local/bin/uwsgi" ]; then
    pip3 install uwsgi
fi

## Make sure the Go development environment is installed.
#
## Make sure curl (utility to get files from the web) is installed.
#if [ ! -f "/usr/bin/curl" ]; then
#    apt install -y curl
#fi
#
#if [ ! -d "/usr/local/go" ]; then
#    if [ ! -f "go1.20.3.linux-amd64.tar.gz" ]; then
#        curl -O https://dl.google.com/go/go1.20.3.linux-amd64.tar.gz
#    fi
#    tar xvf go1.20.3.linux-amd64.tar.gz
#    chown -R root:root ./go
#    mv go /usr/local
#    mkdir $HOME/work
#fi
#
#if [ -z `which go` ]; then
#    echo "Setting Go path..."
#    GOPATH=$HOME/work
#    PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
#fi
#
#
#
## Build the proxy server.
#rm server
#/usr/local/go/bin/go build remote-gateway/server.go
#echo "Running server..."
#./server



echo "Stopping Guacamole..."
systemctl stop guacd

echo "Stopping Tomcat..."
systemctl stop tomcat9

echo "Stopping uWSGI..."
systemctl stop emperor.uwsgi.service

echo "Stopping Nginx..."
systemctl stop nginx

# Make sure the (blank) Guacamole user-mapping file exists.
# os.system("echo > /etc/guacamole/user-mapping.xml")
chmod a+rwx /etc/guacamole/user-mapping.xml

# Copy over the WSGI-based API configuration and code.
cp remote-gateway/emperor.uwsgi.service /etc/systemd/system/emperor.uwsgi.service
chmod 0755 /etc/systemd/system/emperor.uwsgi.service
systemctl daemon-reload

#copyfile("api.py", "/var/lib/nginx/uwsgi/api.py", mode="0755")
#copyfile("client.html", "/var/www/html/client.html", mode="0755")
#copyfile("error.html", "/var/www/html/error.html", mode="0755")


echo "Starting Nginx..."
systemctl start nginx

echo "Starting uWSGI..."
systemctl start emperor.uwsgi.service

echo "Starting Tomcat..."
systemctl start tomcat9

echo "Starting Guacamole server..."
systemctl start guacd
