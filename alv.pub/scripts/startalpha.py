#!/usr/bin/python3
#conding:utf-8
import os,sys
serviceDir='/home/alvin/sophiroth'
#serviceDir='/home/alvin/sophiroth'

portNumber=sys.argv[1]
os.chdir(serviceDir)
startCommand='nohup /usr/bin/python3 -m http.server --cgi %s &>/tmp/%s.log &'%(portNumber,portNumber)
try:
    os.system(startCommand)
    print('Service start up ok.')
except Exception as e:
    print(e)
    print('You should assign a port number as $1')
