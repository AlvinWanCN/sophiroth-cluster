#!usr/bin/python
#_*_coding:utf-8_*_
import subprocess

ip=subprocess.check_output('ip a s|grep global|grep ens|grep 127|cut -d/ -f1|cut -dt  -f2|cut -d" " -f2',shell=True).split('\n')[0]
NICname=subprocess.check_output("ip a s|grep global|grep ens|grep 127|awk '{print $NF}'",shell=True).split('\n')[0]
netFile='/etc/sysconfig/network-scripts/ifcfg-%s'%NICname
if len(NICname) < 3:
    exit(1)
#将dhcp改成static
subprocess.call("sed -i 's/BOOTPROTO=.*/BOOTPROTO=static/' %s "%netFile,shell=True)

ipdict={}
ipdict['IPADDR']=ip
ipdict['NETMASK']='255.255.255.0'
ipdict['GATEWAY']='192.168.127.254'
ipdict['DNS1']='47.75.0.56'
ipdict['DNS2']='114.114.114.114'
ipdict['DOMAIN']='"alv.pub shenmin.com"'

def changeIP(key):
    if subprocess.call('grep %s %s'%(key,netFile),shell=True) == 0:
        subprocess.call("sed -i 's/%s=.*/%s=%s/' %s"%(key,key,ipdict[key],netFile),shell=True)
    else:
        subprocess.call('echo "%s=%s" >> %s'%(key,ipdict[key],netFile),shell=True)

for i in ipdict.keys():
    changeIP(i)

subprocess.call('systemctl restart network',shell=True)