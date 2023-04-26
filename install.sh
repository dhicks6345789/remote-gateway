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



# Make sure the Go development environment is installed.

# Make sure curl (utility to get files from the web) is installed.
if [ ! -f "/usr/bin/curl" ]; then
    apt install -y curl
fi

if [ ! -d "/usr/local/go" ]; then
    if [ ! -f "go1.20.3.linux-amd64.tar.gz" ]; then
        curl -O https://dl.google.com/go/go1.20.3.linux-amd64.tar.gz
    fi
    tar xvf go1.20.3.linux-amd64.tar.gz
    chown -R root:root ./go
    mv go /usr/local
fi

export GOPATH=$HOME/work
export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin



echo "Stopping Guacamole..."
systemctl stop guacd

echo "Stopping Tomcat..."
systemctl stop tomcat9

# Make sure the (blank) Guacamole user-mapping file exists.
# os.system("echo > /etc/guacamole/user-mapping.xml")
chmod a+rwx /etc/guacamole/user-mapping.xml

echo "Starting Tomcat..."
systemctl start tomcat9

echo "Starting Guacamole server..."
systemctl start guacd
