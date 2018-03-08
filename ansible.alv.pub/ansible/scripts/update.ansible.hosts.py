#!/usr/bin/python
#coding:utf-8
import os
url='https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/ansible.alv.pub/ansible/conf.d/hosts'
file='/etc/ansible/hosts'
#serviceName='ansible'
os.system('curl -fsSL %s > %s'%(url,file))
#os.system('systemctl reload %s'%serviceName)