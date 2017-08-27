#!/bin/sh
#****************************************************************#
# ScriptName: change_name.sh
# Create Date: 2014-07-16 16:16
# Modify Date: 2014-07-16 16:16
#***************************************************************#
OLDNAME=$1
NEWNAME=$2
mv /home/http/pub_key/$OLDNAME /home/http/pub_key/$NEWNAME
for a in `who|grep $OLDNAME|awk '{print $2}'`;do pkill -kill -t $a;done
( usermod -l $NEWNAME -d /home/$NEWNAME -m $OLDNAME && groupmod -n $NEWNAME $OLDNAME ) || exit

text="您好，您的堡垒机账号已经修改为您的邮箱域账号，请修改登录堡垒机的用户名，谢谢"
#echo $text|mail -s "堡垒机登录名修改通知" $NEWNAME@jk.cn
