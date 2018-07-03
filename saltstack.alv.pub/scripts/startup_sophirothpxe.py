#coding:utf-8
import subprocess,os

user='alvin'
maindir='/opt/'
project='SophirothPXE'
port=8001
logdir='/var/log/sophirothpxe/'
logfile=logdir+'sophiroth.log'

workdirk=maindir+project

os.chdir(workdirk)
if os.path.exists(logdir):
    pass
else:
    subprocess.call('sudo mkdir -p %s'%logdir, shell=True)
    subprocess.call('sudo chown %s %s'%(user,logdir),shell=True)

subprocess.call('nohup /usr/bin/python3 -m http.server --cgi %s & >>%s &'%(port,logfile),shell=True)
