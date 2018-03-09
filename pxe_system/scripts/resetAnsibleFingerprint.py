#!/usr/bin/python
#coding:utf-8
import os,re
ipstr=os.popen('ip a s ens32|grep global').read() #获取关于ip信息的字符串
ip=re.findall(r'\w\s(.*)\/',ipstr)[0]  #截取ip最后一位
host='http://ansible.alv.pub'
path='/cgi-bin/resetHostFingerprint.py'
querys='user=alvin&host=%s'%ip
url=host + path + '?' + querys

os.system('timeout 3 curl %s'%url)