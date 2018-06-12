###############
samba service
###############

.. contents::

Service State : disabled

Install Samba service
--------------------------

.. code-block:: bash

    yum install samba -y
    [root@saltstack ~]# smbd --version
    Version 4.7.1

Configure samba's config file.
--------------------------------

设置为让该服务器上的用户，可以通过用户名密码访问自己的home目录,这里不需要设置，默认配置就包含了这个功能了。

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

为指定用户添加samba密码
-----------------------
 因为samba服务为了安全起见，是不能用该用户在服务器上的登录密码作为samba密码的，所以需要单独为系统用户指定一个samba密码。

.. code-block:: bash

    [root@saltstack ~]# smbpasswd -a alvin
    New SMB password:
    Retype new SMB password:
    #这里我设置密码为123456

重启服务
---------

然后重启服务，就可以使用我们刚才添加了samba密码的用户alvin登录samba了。

.. code-block::

    systemctl restart smb

linux客户端访问
--------------------


安装客户端工具
+++++++++++++++++++

这里我们需要客户端支持cifs协议，所以安装cifs-utils

.. code-block::

    yum install cifs-utils -y


准备一个用于挂载远程目录的目录
然后挂载

.. code-block:: bash

    [root@dhcp ~]# mkdir /alvinhome
    [root@dhcp ~]# mount -o user=alvin,password=123456 //saltstack.alv.pub/alvin /alvinhome/
    [root@dhcp ~]# df -h /alvinhome/
    Filesystem                 Size  Used Avail Use% Mounted on
    //saltstack.alv.pub/alvin  195G   21G  165G  12% /alvinhome
    [root@dhcp ~]# ls /alvinhome/
    1.py  1.sh  2.sh  cirros-0.3.5-x86_64-disk.img  master  minion  ophira  Python-3.6.4.tar.xz  readme.md  scripts  sophiroth.welcome.py  tmp.py
