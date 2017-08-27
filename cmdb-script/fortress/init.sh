#!/bin/sh
#****************************************************************#
# ScriptName: init.sh
# Create Date: 2014-04-24 14:16
# Modify Date: 2014-04-24 14:16
#***************************************************************#

/bin/rm -f $HOME/.ssh/known_hosts
/bin/rm -f $HOME/.ssh/config

/usr/bin/curl "http://cmdb.mwbyd.cn/api/fortress/userhost/?username=$USER" 2>/dev/null > $HOME/.host_list
echo "" >> $HOME/.ssh/known_hosts
echo "" >> $HOME/.ssh/config

while read line;do
	hostname=`echo $line|/bin/awk '{print $1}'`
	ipaddr=`echo $line|/bin/awk '{print $2}'`
	role=`echo $line|/bin/awk '{print $3}'`
	echo "host $hostname" >> $HOME/.ssh/config
	echo "    hostname $hostname" >> $HOME/.ssh/config
	echo "    port 22" >> $HOME/.ssh/config
	echo "    user $role" >> $HOME/.ssh/config
	echo "" >> $HOME/.ssh/config
done<$HOME/.host_list

/bin/chmod 700 $HOME/.ssh
/bin/chmod 600 $HOME/.ssh/config
