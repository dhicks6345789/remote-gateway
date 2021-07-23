mkdir /etc/guacamole/connections > /dev/null 2>&1
mkdir /etc/guacamole/groups > /dev/null 2>&1

echo STATUS: Syncing data from Google Drive...
rclone --config /root/.config/rclone/rclone.conf sync "drive:Connections" "/etc/guacamole/connections" 2>&1
rclone --config /root/.config/rclone/rclone.conf sync "drive:Groups" "/etc/guacamole/groups" 2>&1
rclone --config /root/.config/rclone/rclone.conf sync "drive:Hosts" "/etc/guacamole/hosts" 2>&1

echo STATUS: Done.
