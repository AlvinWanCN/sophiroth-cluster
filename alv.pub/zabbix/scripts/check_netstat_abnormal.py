#!/usr/bin/python
#coding:utf-8
import os

##检查是否有我们自己设定之外的网络连接出现，没有则返回0，有则返回出现的内容。


basicCommand='netstat -anplut|grep -ivE "connections|Address|10050|10051|801|mysqld|sshd|docker-proxy|pptp|ntpd|slapd|named|wechat|140.207|8003|:53|389"'

content=os.popen(basicCommand).read().split('\n')[:-1]

for i in content:
    print (i)