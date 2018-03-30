#!/usr/bin/python
#coding:utf-8
import subprocess
subprocess.call('curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/Centos7-extras.repo > /etc//yum.repos.d/Centos7-extras.repo')
subprocess.call('yum install epel-release -y')
subprocess.call('yum install salt-minion -y')
subprocess.call("echo 'master: saltstack.alv.pub' > /etc/salt/minion")
subprocess.call('systemctl start salt-minion')
subprocess.call('systemctl enable salt-minion')