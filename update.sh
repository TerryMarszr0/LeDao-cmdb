#!/bin/bash

git remote update -p
git checkout -f origin/master
git submodule update --init
cp configs_ali.py cmdb/configs.py