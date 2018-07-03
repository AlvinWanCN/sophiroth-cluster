#coding:utf-8
import subprocess,os
dir='/opt/SophirothPXE'
os.chdir(dir)
subprocess.call('ls',shell=True)