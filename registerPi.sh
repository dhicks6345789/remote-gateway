# Read user-defined command-line flags.
carryOn=0
while test $# -gt 0; do
    case "$1" in
        -piname)
            shift
            piname=$1
            shift
            ;;
        -y)
            shift
            carryOn=1
            ;;
        *)
            echo "$1 is not a recognized flag."
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
macaddress=`ifconfig | sed -e ':a;N;$!ba;s/\n   / /g' | grep "$ipaddress" | grep -o '..:..:..:..:..:..'`

echo Register Pi
echo ===========
echo Name: "$piname"
echo MAC Address: "$macaddress"
echo IP Address: "$ipaddress"

if [ "$carryOn" -eq "0" ]; then
    echo Stopping - add -y option to continue past this point.
    exit 1;
fi

registerPiResult=`wget http://{{SERVERIPADDRESS}}/registerPi -q -O - --post-data "piName=$piname"`
echo "$registerPiResult"
if [ "$registerPiResult" == "OK" ]; then
    echo RegisterPi - operation completed OK.
else
    echo RegisterPi - operation failed. Message returned: "$registerPiResult"
fi
