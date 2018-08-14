#!usr/bin/python
#_*_coding:utf-8_*_
import subprocess

ip=subprocess.check_output('ip a s|grep global|grep ens|grep 127|cut -d/ -f1|cut -dt  -f2|cut -d" " -f2',shell=True).split('\n')[0]
NICname=subprocess.check_output("ip a s|grep global|grep ens|grep 127|awk '{print $NF}'",shell=True).split('\n')[0]
netFile='/etc/sysconfig/network-scripts/ifcfg-%s'%NICname
if len(NICname) < 3:
    exit(1)
#将dhcp改成static
#subprocess.call("sed -i 's/BOOTPROTO=.*/BOOTPROTO=static/' %s "%netFile,shell=True)
q
# ipdict={}
# ipdict['IPADDR']=ip
# ipdict['NETMASK']='255.255.255.0'
# ipdict['GATEWAY']='192.168.127.254'
# ipdict['DNS1']='192.168.127.3'
# ipdict['DNS2']='114.114.114.114'
# ipdict['DOMAIN']='"alv.pub shenmin.com"'

subprocess.call('nmcli connection modify %s ipv4.address "%s/24" ipv4.gateway 192.168.127.254 ipv4.dns "192.168.127.3 114.114.114.114" ipv4.method manual ipv4.dns-search "alv.pub shenmin.com" '%(NICname,ip),shell=True)
subprocess.call('nmcli connection up %s'%NICname,shell=True)
# def changeIP(key):
#     if subprocess.call('grep %s %s'%(key,netFile),shell=True) == 0:
#         subprocess.call("sed -i 's/%s=.*/%s=%s/' %s"%(key,key,ipdict[key],netFile),shell=True)
#     else:
#         subprocess.call('echo "%s=%s" >> %s'%(key,ipdict[key],netFile),shell=True)
#
# for i in ipdict.keys():
#     changeIP(i)

# subprocess.call('systemctl restart network',shell=True)