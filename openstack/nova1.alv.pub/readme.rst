#################################
nova computer node deployment
#################################



.. contents::

Install nova
`````````````````````````

.. code-block:: bash

    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo
    yum install -y openstack-nova-compute
    yum install -y python-openstackclient openstack-selinux

如果在上面这个操作提示安装包的等级需要升级，就用centos原生网络yum源，可以升级rpm包。


设置Nova实例路径(磁盘镜像文件)
`````````````````````````

.. code-block:: bash

    Vdir=/data/nova
    VHD=$Vdir/instances
    mkdir -p $VHD
    chown -R nova:nova $Vdir



使用QEMU或KVM ,KVM硬件加速需要硬件支持
``````````````````````````````````````````````````

.. code-block:: bash

    [[ `egrep -c '(vmx|svm)' /proc/cpuinfo` = 0 ]] && { Kvm=qemu; } || { Kvm=kvm; }
    echo "使用 $Kvm"
    VncProxy=192.168.127.88  #VNC代理外网IP地址,这里我设置为controller的。



nova配置
`````````````````````````

.. code-block:: bash

    /usr/bin/cp /etc/nova/nova.conf{,.$(date +%s).bak}
    #egrep -v '^$|#' /etc/nova/nova.conf
    echo '#
    [DEFAULT]
    instances_path='$VHD'
    enabled_apis = osapi_compute,metadata
    transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub
    my_ip = 192.168.127.79
    use_neutron = True
    firewall_driver = nova.virt.firewall.NoopFirewallDriver

    [api_database]
    connection = mysql+pymysql://nova:nova@maxscale.alv.pub:4006/nova_api
    [database]
    connection = mysql+pymysql://nova:nova@maxscale.alv.pub:4006/nova

    [api]
    auth_strategy = keystone
    [keystone_authtoken]
    auth_uri = http://keystone1.alv.pub:5000
    auth_url = http://keystone1.alv.pub:35357
    memcached_servers = controller.alv.pub:11211
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    project_name = service
    username = nova
    password = nova

    [vnc]
    enabled = true
    vncserver_listen = 0.0.0.0
    vncserver_proxyclient_address = $my_ip
    novncproxy_base_url = http://'$VncProxy':6080/vnc_auto.html
    [glance]
    api_servers = http://glance1.alv.pub:9292
    [oslo_concurrency]
    lock_path = /var/lib/nova/tmp

    [placement]
    os_region_name = RegionOne
    project_domain_name = Default
    project_name = service
    auth_type = password
    user_domain_name = Default
    auth_url = http://keystone1.alv.pub:35357/v3
    username = placement
    password = placement

    [libvirt]
    #virt_type = '$Kvm'
    virt_type = qemu
    [filter_scheduler]
    scheduler_default_filters=AllHostsFilter

    #'>/etc/nova/nova.conf

    #sed -i 's#nova1.alv.pub:6080#192.168.127.88:6080#' /etc/nova/nova.conf
    #6080 这个vnc地址要写controller的，注意地址。



启动
`````````````````````````

.. code-block:: bash

    systemctl enable libvirtd.service openstack-nova-compute.service
    systemctl restart libvirtd.service openstack-nova-compute.service

















Install neutron compute
```````````````````````````

.. code-block:: bash

    yum install -y openstack-neutron openstack-neutron-ml2 \
    openstack-neutron-linuxbridge python-neutronclient ebtables ipset


Configuration
`````````````````````````
.. code-block:: bash

    cp /etc/neutron/neutron.conf{,.bak}

.. code-block:: bash

    echo '#
    [DEFAULT]
    auth_strategy = keystone
    transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub

    [keystone_authtoken]
    auth_uri = http://keystone1.alv.pub:5000
    auth_url = http://keystone1.alv.pub:35357
    memcached_servers = controller.alv.pub:11211
    auth_type = password
    project_domain_id = default
    user_domain_id = default
    project_name = service
    username = neutron
    password = neutron

    [oslo_concurrency]
    lock_path = /var/lib/neutron/tmp
    #'>/etc/neutron/neutron.conf


在nova计算节点添加配置
``````````````````````````````````````````````````

.. code-block:: bash

    echo '
    #
    [neutron]
    url = http://controller.alv.pub:9696
    auth_url = http://keystone1.alv.pub:35357
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    region_name = RegionOne
    project_name = service
    username = neutron
    password = neutron
    #'>>/etc/nova/nova.conf

    #systemctl restart openstack-nova-api.service

.. code-block:: bash


.. code-block:: bash

    cp /etc/neutron/plugins/ml2/linuxbridge_agent.ini{,bak}


 #ens32是网卡名

.. code-block:: bash

    echo '
    [linux_bridge]
    physical_interface_mappings = provider:ens32
    [securitygroup]
    enable_security_group = true
    firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
    [vxlan]
    enable_vxlan = false
    # local_ip = 10.2.1.21
    # l2_population = true
    #'>/etc/neutron/plugins/ml2/linuxbridge_agent.ini


 #重启相关服务

.. code-block:: bash

    systemctl restart openstack-nova-compute.service
    #启动neutron
    systemctl enable neutron-linuxbridge-agent.service
    systemctl start neutron-linuxbridge-agent.service


openstack客户端查看
`````````````````````````

.. code-block:: bash

    [root@controller ~]# openstack network agent list
    +--------------------------------------+--------------------+--------------------+-------------------+-------+-------+---------------------------+
    | ID                                   | Agent Type         | Host               | Availability Zone | Alive | State | Binary                    |
    +--------------------------------------+--------------------+--------------------+-------------------+-------+-------+---------------------------+
    | 13decfcc-b7a7-45d0-b30d-6f523cc48b7b | Metadata agent     | controller.alv.pub | None              | :-)   | UP    | neutron-metadata-agent    |
    | 1e7d7a40-5cf4-4726-89e0-4fb5396e60a4 | L3 agent           | controller.alv.pub | nova              | :-)   | UP    | neutron-l3-agent          |
    | c637716f-d4af-4275-9333-44525b768afa | Linux bridge agent | controller.alv.pub | None              | :-)   | UP    | neutron-linuxbridge-agent |
    | ede9bef5-4f52-4231-9f74-242f0f50e65b | DHCP agent         | controller.alv.pub | nova              | :-)   | UP    | neutron-dhcp-agent        |
    | f851d1dc-9af8-40ea-b495-54dd343d1d9b | Linux bridge agent | nova1.alv.pub      | None              | :-)   | UP    | neutron-linuxbridge-agent |
    +--------------------------------------+--------------------+--------------------+-------------------+-------+-------+---------------------------+


