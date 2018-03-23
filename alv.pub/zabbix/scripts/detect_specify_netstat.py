#!/usr/bin/python
#coding:utf-8
import sys,os
specified_words=sys.argv
for i in specified_words:
    os.system('netstat -anplut|egrep "%s"'%i)
