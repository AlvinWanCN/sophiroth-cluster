#!/usr/bin/python
#coding:utf=8
import sys,os

num=sys.argv[1]


def n01():
    #item name: 01-update_ansible.alv.pub_ansible_hosts
    os.system('scp /jenkins/workspace/01-update_ansible.alv.pub_ansible_hosts/ansible.alv.pub/ansible/conf.d/hosts ansible:/etc/ansible/hosts')

def n02():
    #item name: 02-update_dc.alv.pub_ldapUserData_alvin_scripts_welcome.py
    os.system('cp /jenkins/workspace/02-update_dc.alv.pub_ldapUserData_alvin_scripts_welcome.py/python/sophiroth.welcome.py /sophiroth/alvin/')
def n03():
    #item name: 03-update_dc.alv.pub_pxe_default
    os.system('scp /jenkins//workspace/03-update_dc.alv.pub_pxe_default/pxe_system/conf.d/default dc:/var/lib/tftpboot/pxelinux.cfg/default')

def n04():
    #item name: 04 - updateAndReload_.alv.pub_named
    pass
    #this item do not use this script
def n05():
    #item name:
    os.system('scp /jenkins/workspace/05-updateAndRestart_dhcp.alv.pub_dhcpd/dhcp.alv.pub/dhcpd/conf.d/dhcpd.conf dhcp:/etc/dhcp/dhcpd.conf')


def main():
    if num == '01':
        n01()
    elif num == '02':
        n02()
    elif num == '03':
        n03()
    elif num == '04':
        n04()
    elif num == '05':
        n05()
    else:
        pass


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Detected error, details as follows:')
        print(e)