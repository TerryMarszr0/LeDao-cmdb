#version_1.0
#!/bin/bash
source /etc/profile
homedir="/home/deploy"
ENV=$2
app_flag="cmdb_$ENV"
str=$"/n"  

function help() {
  echo "Usage: $0 start|stop"
}

function start(){
    echo "copy configs.py"
    cp -f configs_$ENV.py cmdb/configs.py

    echo "copy static file"
expect << EOF
    set timeout 5
    spawn python manage.py collectstatic
    send "yes"
    send "\r"
    expect eof
EOF

    nohup uwsgi --ini uwsgi.ini --ignore-sigpipe > /dev/null &
    sstr=$(echo -e $str)
    echo "$sstr"
    sleep 5
    echo "MW_SUCCESS"
}


function stop(){
    pid=`ps aux | grep uwsgi.ini | grep -v grep | awk '{print $2}'`
    ps aux | grep uwsgi.ini | grep -v grep | awk '{print $2}' | xargs kill -9
    echo "cmdb $pid killed"
    echo "MW_SUCCESS"
}

#输入提示
if [ "$1" == "" ]; then
  help
elif [ "$1" == "stop" ]; then
  stop
elif [ "$1" == "start" ]; then
  start
else
  help
fi
