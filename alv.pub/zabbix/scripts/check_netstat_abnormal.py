#!/usr/bin/python
#coding:utf-8
import os

##检查是否有我们自己设定之外的网络连接出现，没有则返回0，有则返回出现的内容。


basicCommand='netstat -anplut|grep -ivE "180.169.223.10|connections|Address|1005|alvin|801|mysqld|sshd|1281|docker-proxy|32000|AliYunDUn|pptp|ntpd|slapd|named|100.100|wechat|140.207|183.3|8003|3306|:53"'
command1=basicCommand+'|wc -l'
#command2='netstat -anplut|grep -ivE "180.169.223.10|connections|Address|1005|alvin|801|mysqld|sshd|1281|docker-proxy|32000|AliYunDUn|pptp|ntpd|slapd|named|100.100|wechat|140.207|183.3|8003|3306"'


lineNumber=os.popen(command1).read().split('\n')[0]
content=os.popen(basicCommand).read().split('\n')[:-1]
if lineNumber == '0':
    print(0)
else:
    for i in content:
        print (i)