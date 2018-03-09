#!/usr/bin/python
#coding:utf-8
import os,re,urllib2,socket
hostname=socket.gethostname().split('.')[0]
host='http://ansible.alv.pub'
path='/cgi-bin/resetHostFingerprint.py'
querys='user=alvin&host=%s'%hostname
url=host + path + '?' + querys
urllib2.urlopen(url)
