docker-latest
############################

Install docker-latest
===============================

.. code-block:: bash

    $ sudo yum install docker-latest

Start docker-latest and enable
=========================================

.. code-block:: bash

    $ sudo systemctl start docker-latest
    $ sudo systemctl enable docker-latest

l2tp/ipsec vpn
========================

.. code-block:: bash

    $ sudo modprobe af_key
    $ vim vpn.env
    VPN_IPSEC_PSK=your_ipsec_pre_shared_key
    VPN_USER=your_vpn_username
    VPN_PASSWORD=your_vpn_password
    $ sudo docker run \
        --name ipsec-vpn-server \
        --env-file ./vpn.env \
        --restart=always \
        -p 500:500/udp \
        -p 4500:4500/udp \
        -v /lib/modules:/lib/modules:ro \
        -d --privileged \
        hwdsl2/ipsec-vpn-server

your server have firewall setting, you should open udp port 500 and 4500 at firewall.


nginx
==========

#. 创建并启动我的docker nginx容器

    config 目录用于存放nginx配置的，logs目录存放日志。

    .. code-block:: bash

        $ sudo mkdir -p /home/alvin/docker_service/nginx/
        $ cd /home/alvin/docker_service/nginx/
        $ sudo mkdir -p {config,logs,www}
        $ ls
        config  logs  www
        $ sudo curl -s https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/alv.pub/docker-latest/nginx/conf.d/alv.pub.conf > config/alv.pub.conf
        $ cat config/alv.pub.conf

    .. literalinclude:: ./nginx/conf.d/alv.pub.conf
        :language: conf
        :linenos:
        :lines: 1-


#. 启动nginx容器

    .. code-block:: bash

        $ sudo docker run -d -it \
         -p 80:80 -p 443:443 \
         -v `pwd`/www:/www \
         -v `pwd`/config:/etc/nginx/conf.d \
         -v `pwd`/logs:/var/log/nginx \
         -v /etc/localtime:/etc/localtime \
         --name nginx \
         --privileged=true \
         --restart=always \
         nginx
        $ sudo docker exec -it nginx bash
        # grep client_max_body_size /etc/nginx/nginx.conf ||sed -i '23a client_max_body_size 500m;' /etc/nginx/nginx.conf
        # exit
        $ sudo docker restart nginx



