sophiroth-pxe service
########################


Install sophiroth pxe
```````````````````````````

.. code-block:: bash

    cd /opt/
    git clone https://github.com/AlvinWanCN/sophiroth-pxe.git


add user and grant sudo
`````````````````````

需要用拥有sudo权限的非root用户执行，因为如果是root用户执行的，则实际cgi user会变成nobody。

所以这里我们创建sophiroth-pxe用户，并授予sudo权限。
.. code-block:: bash

useradd sophiroth-pxe -s /sbin/nologin
echo "sophiroth-pxe ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/sophiroth-pxe

add configuration file for start sophroth-pxe
``````````````````````````````````````````````````````

根据python版本来写启动命令，下面分别是python2和3的启动命令。

* /usr/bin/python2 -m CGIHTTPServer 8001
* /usr/bin/python3 -m http.server --cgi 8001

我们根据实际使用的python版本来决定在下面的启动配置文件里写哪一条，这里我们用的是python2的。

.. code-block:: bash

    echo '
    [Unit]
    Description=The Sophiroth Service
    After=syslog.target network.target salt-master.service

    [Service]
    Type=simple
    User=alvin
    WorkingDirectory=/opt/sophiroth-pxe
    ExecStart=/usr/bin/python2 -m CGIHTTPServer 8001
    KillMode=process
    Restart=on-failure
    RestartSec=3s

    [Install]
    WantedBy=multi-user.target graphic.target
    ' > /usr/lib/systemd/system/sophiroth-pxe.service

startup sophroth-pxe
```````````````````````````

.. code-block:: bash

    systemctl enable sophiroth-pxe
    systemctl start sophiroth-pxe
    systemctl status sophiroth-pxe
    lsof -i:8001


这里我们是指定了端口为tcp 8001端口

