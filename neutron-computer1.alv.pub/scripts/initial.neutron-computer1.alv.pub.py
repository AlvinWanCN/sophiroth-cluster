#!/usr/bin/python
#coding:utf-8
import os
os.system('wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo')
os.system('yum install centos-release-openstack-pike -y')
os.system("sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo")
os.system('yum install -y openstack-neutron openstack-neutron-ml2 openstack-neutron-linuxbridge python-neutronclient ebtables ipset')

os.system('cp /etc/neutron/neutron.conf{,.bak}')