#!/usr/bin/python
#coding:utf-8
import socket,os
hostname=socket.gethostname()

def initital_host(host):
    url='https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/%s/scripts/initial.%s.py'%(host,host)
    os.system('curl -fsSL ')