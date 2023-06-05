# Read user-defined command-line flags.
while test $# -gt 0; do
    case "$1" in
        -piname)
            shift
            piname=$1
            shift
            ;;
        *)
            echo "$1 is not a recognized flag!"
            exit 1;
            ;;
    esac
done

# Check all required flags are set, print a usage message if not.
if [ -z "$piname" ]; then
    echo "Usage: registerPi.sh -piname PINAME"
    echo "PINAME: The display name of the Raspberry Pi you want to register (e.g. MY-PI01)"
    exit 1;
fi

ipaddress=`hostname -I`
# macaddress=`ifconfig | sed -e ':a;N;$!ba;s/\n   / /g' | grep "$ipaddress" | grep -o '..:..:..:..:..:..:..:..'`
macaddress=`ifconfig | sed -e ':a;N;$!ba;s/\n   / /g'`

echo Register Pi
echo ===========
echo Name: "$piname"
echo MAC Address: "$macaddress"
echo IP Address: "$ipaddress"
