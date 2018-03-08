#!/usr/bin/python
#coding:utf-8
import os
dir='/root/.ssh/'
if os.path.exists(dir):
    pass
else:
    os.mkdir(dir)
file=os.path.join(dir,'authorized_keys')

#ansible 服务器公钥
ansiblePubKey='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDqZ53fbpr7oHooLRtlkD6w5EyuV3XjkPywtlAlhSbY1FAMfpQvEzRYOa0W4C6delrkM1qnH0XaZbLK3qrdap/hDa/dIH8pGXCLar/4Aznsln91SYIkDwSuf03TSKu/Hjz7+JX5t1K0fdmZ/5F+d+ZGpb+jVIp+oakglGhJghV5RR+Fu+aFEEwJseHOSzUfu5uHM4biUTfUml/cRpcsLnh9t4A50nhAgM18mZwBlQiQwofiez1zi6zXuur9fFpbNvURW+Tpr5cCmafSX99H6aq1YcbXANWSmBmPr6kp9ZTNxo+VC6z44qjBu6DMC6rf/pGrSdIJ3CUNDVaQvD4eqovn root@ansible.alv.pub\n'

wtfile=open(file,'a') #打开文件
wtfile.write(ansiblePubKey) #将公钥写入文件
wtfile.close() #关闭文件