mkdir /etc/guacamole/connections > /dev/null 2>&1
mkdir /etc/guacamole/groups > /dev/null 2>&1

echo STATUS: Syncing data from Google Drive...
rclone --config .config\rclone\rclone.conf sync "drive:connections" "/etc/guacamole/connections" 2>&1

echo STATUS: Done.
