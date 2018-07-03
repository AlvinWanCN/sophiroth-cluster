#!/usr/bin/python
#coding:utf-8
import os,time
url='https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/dns.alv.pub/named/conf.d/alv.pub.zone'
file='/var/named/alv.pub.zone'
serviceName='named'
os.system('curl -fsSL %s > %s'%(url,file))
time.sleep(3)
os.system('systemctl restart %s'%serviceName)