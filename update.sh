#!/bin/bash

rm -fR cmdb.bak
cp -R cmdb cmdb.bak
cd /home/deploy/cmdb

git remote update -p
git checkout -f origin/master
git submodule update --init
cp /home/deploy/cmdb.conf /home/deploy/cmdb