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
okPiResult=`echo "$registerPiResult" | grep -o "OK-"`
if [ "$okPiResult" == "OK-" ]; then
    vncPassword=`echo "$registerPiResult" | tail -c 9`
    echo RegisterPi - operation completed OK.
    echo "$registerPiResult"
    echo "$vncPassword"
    
    # Enable SSH, add the server's public key to the local authorized_keys so the server has access to this device.   
    sudo systemctl enable ssh
    sudo systemctl start ssh
    serverPublicKey=`wget http://{{SERVERIPADDRESS}}/getPublicKey -q -O -`
    mkdir -p ~/.ssh
    echo "$serverPublicKey" >> ~/.ssh/authorized_keys
    
    # Enable VNC.
    sudo systemctl enable vncserver-x11-serviced.service
    sudo systemctl start vncserver-x11-serviced.service
    authenticationGrep=`sudo cat /root/.vnc/config.d/vncserver-x11 | grep Authentication=VncAuth`
    if [ "$authenticationGrep" == "" ]; then
        sudo bash -c "echo Authentication=VncAuth >> /root/.vnc/config.d/vncserver-x11"
        sudo bash -c "echo Encryption=AlwaysOff >> /root/.vnc/config.d/vncserver-x11"
        # sudo bash -c "echo ProtocolVersion=4.1 >> /root/.vnc/config.d/vncserver-x11"
    fi
    echo "$vncPassword" | sudo vncpasswd -service -legacy
else
    echo RegisterPi - operation failed. Message returned:
    echo "$registerPiResult"
fi
