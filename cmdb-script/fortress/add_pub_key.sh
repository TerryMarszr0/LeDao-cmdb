#!/bin/sh
#****************************************************************#
# ScriptName: add_pub_key.sh
# Create Date: 2014-04-24 16:43
# Modify Date: 2014-04-24 16:43
#***************************************************************#

username=$1
role=$2
mkdir -p /home/$role/.ssh
chown -R $role /home/$role/

sed -i "/$username@/"d /home/$role/.ssh/authorized_keys

curl "10.0.128.245/pub_key/$username" 2>/dev/null >> /home/$role/.ssh/authorized_keys

chmod -R 700 /home/$role/.ssh
