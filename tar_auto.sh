#!/bin/bash
source /etc/profile

PROJECT_NAME="cmdb_deploy"
mkdir $PROJECT_NAME
mv * .[^.]* $PROJECT_NAME
tar -czvf  "$PROJECT_NAME".tar.gz  $PROJECT_NAME/
check $?
echo "MW_SUCCESS"
