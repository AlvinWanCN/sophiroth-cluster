#!/usr/bin/python
#coding:utf-8
import os
os.system('yum install https://downloads.mariadb.com/MaxScale/2.1.9/rhel/7/x86_64/maxscale-2.1.9-1.rhel.7.x86_64.rpm -y')
os.system('maxkeys /var/lib/maxscale/ ')
os.system('curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/maxscale.alv.pub/maxscale/conf.d/maxscale.conf > /etc/maxscale.cnf')
os.system('chown maxscale /var/lib/maxscale/ -R')