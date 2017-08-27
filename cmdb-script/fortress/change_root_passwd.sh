#!/bin/sh

USER_MAIL="chenshaodong@hys-inc.cn xiejunmin@hys-inc.cn zyb@hys-inc.cn zhangfangyan@hys-inc.cn"
#RELAY_LIST="10.0.128.25 10.0.128.24 10.129.8.16 10.129.8.20"
PASSWD=`openssl rand -base64 11`
#PASSWD=`date +%s | sha256sum | base64 | head -c 11`

echo "$PASSWD"| passwd --stdin root

text="10.0.128.25 堡垒机root密码变更为：$PASSWD"

for mail in $USER_MAIL
do
    echo $text|mail -s "堡垒机密码变更" $mail
done
