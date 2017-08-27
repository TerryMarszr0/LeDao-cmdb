#!/bin/sh
#****************************************************************#
# ScriptName: relay.sh
# Create Date: 2014-03-31 13:55
# Modify Date: 2014-03-31 13:55
#***************************************************************#

username=$1
passwd=$2

path='/opt/cmdb-script/fortress'
#passwd=`date +%s%N | md5sum | head -c 10`

if [ "$username" != "" ];then
	google_url=`/bin/sh $path/useradd.sh $username $passwd 2>/dev/null |grep "https://www.google.com"`
else
	echo "no username"
fi
echo $google_url
echo $google_url > /bdata/tmp/$username
