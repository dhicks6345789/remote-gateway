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

#echo "Servername: $servername";
#echo "Database password: $databasepw";
#echo "Guacamole password: $guacpw";

# Use Chase Wright's script to install a Guacamole server - see: https://github.com/MysticRyuujin/guac-install
if [ ! -f "guac-install.sh" ]; then
    wget https://git.io/fxZq5 -O guac-install.sh
    chmod +x guac-install.sh
    #./guac-install.sh --mysqlpwd " + userOptions["-databasePassword"] + " --guacpwd " + userOptions["-guacPassword"] + " --nomfa --installmysql
fi
