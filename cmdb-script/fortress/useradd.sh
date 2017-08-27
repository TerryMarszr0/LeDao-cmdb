#!/bin/sh
#****************************************************************#
# ScriptName: useradd.sh
# Create Date: 2014-03-31 09:43
# Modify Date: 2014-03-31 09:43
#***************************************************************#
username=$1
passwd=$2

userdel -f $username
useradd $username -s /opt/cmdb-script/fortress/fortress.py

mkdir -p /home/$username/bin/
rm -rf /home/$username/bin/*
rm -rf /home/$username/.ssh/*

expect << EOF
	set timeout 5
	spawn passwd $username
	expect "New password:"
	send $passwd
	send "\r"
	expect "Retype new password:"
	send $passwd
	send "\r"
	expect eof
EOF

#expect << EOF
#	set timeout 5
#	spawn sudo -u $username /usr/bin/google-authenticator
#	expect "(y/n)"
#	send "y\r"
#	expect "(y/n)"
#	send "y\r"
#	expect "(y/n)"
#	send "y\r"
#	expect "(y/n)"
#	send "y\r"
#	expect "(y/n)"
#	send "y\r"
#	expect eof
#EOF

expect << EOF
	set timeout 5
	spawn sudo -u $username /usr/bin/ssh-keygen
	expect "Enter file"
	send "\r"
	expect "Enter passphrase"
	send "\r"
	expect "Enter same passphrase"
	send "\r"
	expect eof
EOF

rm -rf /bdata/http/pubkey/$username
cp /home/$username/.ssh/id_rsa.pub /bdata/http/pubkey/$username

chown -R $username /home/$username
#rm -f /home/$username/.bash_profile
#cp /opt/cmdb-script/fortress/.bash_profile /home/$username/
chown $username /home/$username/.bash_profile

cp /opt/cmdb-script/fortress/init.sh /home/$username/bin/
ln -s /usr/bin/ssh /home/$username/bin/ssh
ln -s /usr/bin/passwd /home/$username/bin/passwd
ln -s /bin/logger /home/$username/bin/logger
ln -s /bin/awk /home/$username/bin/awk
ln -s /bin/sort /home/$username/bin/sort
ln -s /bin/sed /home/$username/bin/sed
ln -s /usr/bin/pssh /home/$username/bin/pssh
#chown $username /home/$username/bin/*
