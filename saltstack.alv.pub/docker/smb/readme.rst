##################
smb container
##################


.. contents::


创建编写docker file
``````````````````````

.. code-block:: bash

    [root@saltstack ~]# cat Dockerfile
    FROM centos:6.9

    # MAINTAINER_INFO
    MAINTAINER Alvin Wan <alvin.wan.cn@hotmail.com>
    RUN yum install samba -y
    RUN mkdir -p /samba
    RUN chmod 777 /samba
    RUN useradd user1
    RUN useradd user2
    RUN echo -e "smbpasswd -a user1\nsophiroth\nsophiroth"|bash
    RUN echo -e "smbpasswd -a user2\nsophiroth\nsophiroth"|bash
    RUN echo '[samba]'>> /etc/samba/smb.conf
    RUN echo 'path = /samba' >> /etc/samba/smb.conf
    RUN echo 'browseable = no' >> /etc/samba/smb.conf
    RUN echo 'writable = yes' >> /etc/samba/smb.conf
    RUN echo 'guest ok = yes' >> /etc/samba/smb.conf
    RUN sed -i 's/security = user/security = share/' /etc/samba/smb.conf
    RUN echo -e "[user1]\nsecurity = user\npath = /user1\nbrowseable = no\nwritable = yes\nvalid users = user1" >> /etc/samba/smb.conf
    RUN echo -e "[user2]\nsecurity = user\npath = /user2\nbrowseable = no\nwritable = yes\nvalid users = user2" >> /etc/samba/smb.conf
    ADD smb.sh /smb.sh
    #ENTRYPOINT ["/smb.sh"]
    ENTRYPOINT /etc/init.d/smb start &&  /bin/bash

创建镜像
```````````````

当前目录是存放dockerfile的目录

.. code-block:: bash

    docker build -t smb3 .



创建本地目录
```````````````````````

创建本地目录用于映射到容器里面去

.. code-block:: bash

    mkdir -p {/samba,/user1,/user2}


创建容器
````````````````

.. code-block:: bash

    docker run -d -it   -v /etc/localtime:/etc/localtime  -p 445:455 -p 137:137 -p 138:138 -p 139:139  -v /samba:/samba -v /user1:/user1 -v /user2:/user2 --hostname samba.alv.pub --name smb  smb3



客户端访问
``````````````````


windows客户端访问
--------------------

 资源管理器地址栏输入\\saltstack.alv.pub\user1 输入用户名user1，密码sophiroth， 会访问到容器里面的user1的home目录

  资源管理器地址栏输入\\saltstack.alv.pub\user2 输入用户名user2，密码sophiroth， 会访问到容器里面的user2的home目录
