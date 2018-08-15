#!/usr/bin/python
#coding:utf-8
import os
#
os.system('curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/galera.repo > /etc/yum.repos.d/galera.repo') #add mariadb galera cluster repository
os.system('yum install MariaDB-Galera-server -y') #install mariadb-galera-server
os.system('curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/db1.alv.pub/galera-mariadb/conf.d/server.cnf > /etc/my.cnf.d/server.cnf')
os.system('/etc/init.d/mysql start --wsrep-new-cluster')
