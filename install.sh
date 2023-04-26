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

if [ -z "$servername" ] || [ -z "$databasepw" ] || [ -z "$guacpw" ]; then
    echo "Usage: install.sh -servername"
    exit 1;
fi

echo "Servername: $servername";
echo "Database password: $databasepw";
echo "Guacamole password: $guacpw";
