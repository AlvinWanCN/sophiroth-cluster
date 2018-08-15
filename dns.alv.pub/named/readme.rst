bind
#########

这里我们使用的软件是bind, 安装后的服务是named，提供dns服务。

这里要注意的是，如果我们的dns服务器是能通过外网直接访问到的，而我们的目的不是对外公共提供服务的，那我们需要设置好防火墙规则。

dns服务是使用的udp协议53号端口，一个客户端就可以通过该端口占用dns服务器不小的流量。

所以我们需要让udp 53号端口只提供给我们允许的IP访问。


安装bind
=============

.. code-block:: bash

    yum install named -y

配置
=========

.. code-block:: bash

    $ sudo curl -s https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/dns.alv.pub/named/conf.d/named.conf > /etc/named.conf
    $ sudo curl -s https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/dns.alv.pub/named/conf.d/named.rfc1912.zones > /etc/named.rfc1912.zones
    $ sudo curl -s https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/dns.alv.pub/named/conf.d/alv.pub.zone > /var/named/alv.pub.zone
    $ sudo curl -s https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/dns.alv.pub/named/conf.d/shenmin.com.zone > /var/named/shenmin.com.zone
    $ sudo chown named:named /var/named/*
    $ sudo chgrp named /etc/named.conf


重启服务
=============

.. code-block:: bash

    $ sudo systemctl restart named

防火墙开启允许dns
=======================

.. code-block:: bash

    $ sudo firewall-cmd --add-service=dns --permanent
    $ sudo firewall-cmd --reload



配置详细内容
================

- /var/named/alv.pub.zone的内容

.. literalinclude:: ./conf.d/alv.pub.zone
    :language: zone
    :linenos:
    :lines: 1-




