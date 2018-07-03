#coding:utf-8
import subprocess,os

maindir='/opt/'
project='SophirothPXE'
workdirk=maindir+project
port=8001
logdir='/var/log/sophirothpxe/'
logfile=logdir+'sophiroth.log'

os.chdir(workdirk)
subprocess.call('mkdir -p %s'%logdir,shell=True)
subprocess.call('nohup /usr/bin/python3 -m http.server --cgi %s & >>%s &'%(port,logfile),shell=True)
