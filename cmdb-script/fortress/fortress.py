#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import getpass
import re
import time
import pexpect
import termios
import struct
import fcntl
import signal
import sys, os

domain = 'cmdb.mwbyd.cn'

def ip_format_chk(ip):
    if ip == "":
        return True
    pattern = r"^\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b$"
    if re.match(pattern, ip):
        return True
    else:
        return False


def hostname_format_chk(hostname):
    if hostname == "":
        return True
    pattern = r"^[0-9a-z\-]+.\.[0-9a-z\-]+$"
    if re.match(pattern, hostname):
        return True
    else:
        return False


def relay_help():
    print '''
    If u have any problem with fortress host, contact with group.yunwei@puscene.com
    1.list all host info
    2.piliang
    3.grep hosts by key
    4.help info
    5.refresh host list
    0.exit
    Others:input ip address or hostname to connect to host
    if you want to connect to host by your account not default(root/deploy), add your account after host split by space,for example:10.128.2.48 account'''


def get_all_host_list(username):
    print "try to get host list..."
    try:
        header = {'Content-Type': "application/x-www-form-urlencoded"}
        response = requests.get('http://' + domain + '/api/fortress/userhost/?format=json&limit=10000&username=' + username, {}, headers=header)
        if response.status_code == 200:
            result_body = json.loads(response.text)
            return result_body['results']
        else:
            return []
    except Exception, e:
        return []


def get_host_list_by_app(app_name):
    h_list = []
    try:
        header = {'Content-Type': "application/x-www-form-urlencoded"}
        response = requests.get('http://' + domain + '/api/host/host/?format=json&limit=1000&service_name=' + app_name, {}, headers=header)
        if response.status_code == 200:
            result_body = json.loads(response.text)
            for h in result_body['results']:
                h_list.append(h['ip'])
        return h_list
    except Exception, e:
        print "get host_list error:" + str(e)
    return h_list


def grep_list_info(k, all_host):
    for j in range(0, len(all_host)):
        h1 = all_host[j]
        if k in h1['hostname']:
            print "%-8s\t%-30s\t%-15s ===> %-6s" % (
                "["+echo_ret("a"+str(j))+"] ", h1['hostname'], h1['ip'], h1['role'])


def ssh_connect(k, all_host):
    tmp_l = k.split(" ")
    if len(tmp_l) == 2:
        k1 = tmp_l[0]
        role = tmp_l[1]
        pexpect_ssh(k1, role)
    else:
        for h1 in all_host:
            if h1['ip'] == k or h1['hostname'] == k:
                pexpect_ssh(k, h1['role'])
                break
        else:
            print "host not in list, default root"
            pexpect_ssh(k, "root")
            print "logout"


def ssh_command(key, command):
    global all_host_list
    for host in all_host_list:
        if host['ip'] == key or host['hostname'] == key:
            pexpect_ssh(key, host['role'], command)


# add by taoshoukun
def c_echo(content, color='green'):
    if color == 'green':
        print '\033[32m%s\033[0m' % content
    elif color == 'red':
        print '\033[31m%s\033[0m' % content
    elif color == 'blue':
        print '\033[31m%s\033[0m' % content
    elif color == 'yel':
        print '\033[33%s\033[0m' % content
    elif color == 'yel':
        print '\033[33%s\033[0m' % content


def echo_ret(content, color='green'):
    if color == 'green':
        return '\033[32m%s\033[0m' % content
    elif color == 'red':
        return '\033[31m%s\033[0m' % content
    elif color == 'blue':
        return '\033[31m%s\033[0m' % content
    elif color == 'yel':
        return '\033[33%s\033[0m' % content
    elif color == 'yel':
        return '\033[33%s\033[0m' % content


def get_win_size():
    """This function use to get the size of the windows!"""
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        # Assume
        TIOCGWINSZ = 1074295912L
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]


def sigwinch_passthrough(sig, data):
    """NOTICE: sig,data can't del.If del,you can't connect in second time"""
    winsize = get_win_size()
    pssh.setwinsize(winsize[0], winsize[1])


def pexpect_ssh(login_host, login_user, cmd_option=""):
    try:
        logfile = open("%s/%s_%s_%s_log" % (log_dir, username, time.strftime('%Y%m%d'), login_host), 'a')
        logfile.write('\n\n%s\n\n' % time.strftime('%Y%m%d_%H%M%S'))
        cmd = 'export SSH_SHTERM_NAME=%s;ssh -o ConnectTimeout=30 -o SendEnv=SSH_SHTERM_NAME %s@%s "%s"' % (
            username.encode('utf-8'), login_user.encode('utf-8'), login_host.encode('utf-8'), cmd_option.encode('utf-8'))
        global pssh
        pssh = pexpect.spawn('/bin/bash', ['-c', cmd])
        pssh.logfile = logfile
        c_echo("login For:"+login_host+" for:"+login_user)
        signal.signal(signal.SIGWINCH, sigwinch_passthrough)
        size = get_win_size()
        pssh.setwinsize(size[0], size[1])
        pssh.interact(escape_character=None)
        # pssh.sendcontrol("]")
    except Exception, e:
        c_echo("            exception!!!                please input exit, then retry, thank you!", color="red")


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    log_dir = "/bdata/fortresslog/"

    username = getpass.getuser()
    log_dir += username
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    all_host_list = get_all_host_list(username)
    relay_help()

    try:
        while True:
            try:
                content = raw_input('\nPlease input your choice:')
            except (KeyboardInterrupt, EOFError):
                content = "\n"
            print "\n"
            tmp_list = content.split(" ")
            if content == "1":
                # list all host info
                count = 0
                for h in all_host_list:
                    print "%-6s\t%-15s\t%-8s\t%-20s\t%-45s ===> %-6s" % (
                        "[" + echo_ret("a" + str(count)) + "] ", h['ip'], h['env'],
                        h['room_name'], h['hostname'], h['role'])
                    count += 1

            elif content == "2":
                # piliang
                try:
                    all_str = raw_input(u'\nPlease input host list(split by ,) or app name, then your command:')
                    print all_str

                    all_list = all_str.split(" ")

                    if all_list[0].count(",") > 0 or ip_format_chk(all_list[0]):
                        host_list = all_list[0].split(",")
                    else:
                        app = all_list[0]
                        host_list = get_host_list_by_app(app)
                    command_list = all_list[1:]
                    commands = ""

                    for command in command_list:
                        commands = commands + " " + command
                    s_tag = 1

                    for host in host_list:
                        if not (ip_format_chk(host) or hostname_format_chk(host)):
                            s_tag = 0
                            print "input error, exit"

                    if s_tag == 1:
                        for host in host_list:
                            print host
                            ssh_command(host, commands)

                    relay_help()
                except Exception, e:
                    print "piliang_error:"+str(e)
                    relay_help()
            elif content == "3":
                # grep hosts by key
                try:
                    key = raw_input('\nPlease input key:')
                    grep_list_info(key, all_host_list)
                except Exception, e:
                    print e
                    relay_help()
            elif content == "" or content == "4":
                # help info
                relay_help()
            elif content == "5":
                # refresh host list
                all_host_list = get_all_host_list(username)
            elif content == "exit" or content == "0":
                # exit
                break
            elif re.match("^a([0-9]*[0-9])$", content):
                m = re.match("^a([0-9]*[0-9])$", content)
                if int(m.group(1)) <= len(all_host_list):
                    try:
                        ssh_connect(all_host_list[int(m.group(1))]['ip'], all_host_list)
                    except Exception, e:
                        print e
                        print "logout"
                relay_help()
            elif ip_format_chk(tmp_list[0]) or hostname_format_chk(tmp_list[0]):
                try:
                    ssh_connect(content, all_host_list)
                except Exception, e:
                    print e
                    print "logout"
                relay_help()
            else:
                print "your input error"
        print "\next the session"
    except Exception, e:
        print "\next the session"
        print e
