#!/usr/bin/python
#coding:utf-8
import subprocess
subprocess.call('curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/Centos7-extras.repo > /etc//yum.repos.d/Centos7-extras.repo',shell=True)
subprocess.call('yum install epel-release -y',shell=True)
subprocess.call('yum install salt-minion -y',shell=True)
subprocess.call("echo 'master: saltstack.alv.pub' > /etc/salt/minion",shell=True)
subprocess.call('systemctl start salt-minion',shell=True)
subprocess.call('systemctl enable salt-minion',shell=True)