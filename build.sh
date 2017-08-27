#!/bin/bash
source /etc/profile

if [ ! $1 ];then
    echo "Usage: $0 enviroment"
    exit 1
fi

ENV=$1
echo "$ENV"
PROJECT_NAME="cmdb_$ENV"

function check() {
  if [ $1 != 0 ];then
    echo "exec fail"
    exit 1
  fi
}

sed -i "s/xxx/$ENV/g" service.sh
mkdir $PROJECT_NAME
mv * .[^.]* $PROJECT_NAME
tar -czvf  "$PROJECT_NAME".tar.gz  $PROJECT_NAME/
check $?
echo "MW_SUCCESS"
