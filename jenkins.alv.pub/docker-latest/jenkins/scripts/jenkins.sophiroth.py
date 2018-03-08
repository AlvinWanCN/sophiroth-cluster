#!/usr/bin/python
#coding:utf=8
import sys

num=sys.argv[1]


def n01():
    #item name: 01-update_ansible.alv.pub_ansible_hosts
    print('01')

def n02():
    #item name: 02-update_dc.alv.pub_ldapUserData_alvin_scripts_welcome.py
    print('02')




def main():
    if num == '01':
        n01()
    elif num == '02':
        n02()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Detected error, details as follows:')
        print(e)