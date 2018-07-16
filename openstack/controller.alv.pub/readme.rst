################################
controller.alv.pub
################################


.. contents::


参考资料
````````````````````

url: https://www.cnblogs.com/elvi/p/7613861.html


添加openstack的仓库
```````````````````````
.. code-block:: bash

    python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/common_tools/pullLocalYum.py)" #add local basic repository
    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo





创建 OpenStack 客户端环境脚本
----------------------------------------------


.. code-block:: bash

    echo "
    export OS_PROJECT_DOMAIN_NAME=default
    export OS_USER_DOMAIN_NAME=default
    export OS_PROJECT_NAME=admin
    export OS_USERNAME=admin
    export OS_PASSWORD=admin
    export OS_AUTH_URL=http://keystone1.alv.pub:35357/v3
    export OS_IDENTITY_API_VERSION=3
    export OS_IMAGE_API_VERSION=2
    ">./admin-openstack.sh


测试脚本是否生效
----------------------------------------------

.. code-block:: bash

    source ./admin-openstack.sh
    yum install python-openstackclient openstack-selinux python2-PyMySQL -y #OpenStack客户端
    yum install openstack-utils -y #openstack工具
    openstack token issue


创建service项目,创建glance,nova,neutron用户，并授权
---------------------------------------------------------------------

.. code-block:: bash

    openstack project create --domain default --description "Service Project" service
    openstack user create --domain default --password=glance glance
    openstack role add --project service --user glance admin
    openstack user create --domain default --password=nova nova
    openstack role add --project service --user nova admin
    openstack user create --domain default --password=neutron neutron
    openstack role add --project service --user neutron admin


创建demo项目(普通用户密码及角色)
----------------------------------------------

.. code-block:: bash

    openstack project create --domain default --description "Demo Project" demo
    openstack user create --domain default --password=demo demo
    openstack role create user
    openstack role add --project demo --user demo user


demo环境脚本
-----------------------

.. code-block:: bash

    echo "
    export OS_PROJECT_DOMAIN_NAME=default
    export OS_USER_DOMAIN_NAME=default
    export OS_PROJECT_NAME=demo
    export OS_USERNAME=demo
    export OS_PASSWORD=demo
    export OS_AUTH_URL=http://keystone1.alv.pub:5000/v3
    export OS_IDENTITY_API_VERSION=3
    export OS_IMAGE_API_VERSION=2
    ">./demo-openstack.sh


测试脚本是否生效
----------------------------------------------

.. code-block:: bash

    source ./demo-openstack.sh
    openstack token issue


安装配置glance
``````````````````````````



创建Glance数据库、用户、认证，前面已设置
---------------------------------------------------------------------

 keystone上服务注册 ,创建glance服务实体,API端点（公有、私有、admin）

.. code-block:: bash

    source ./admin-openstack.sh || { echo "加载前面设置的admin-openstack.sh环境变量脚本";exit; }
    openstack service create --name glance --description "OpenStack Image" image
    openstack endpoint create --region RegionOne image public http://glance1.alv.pub:9292
    openstack endpoint create --region RegionOne image internal http://glance1.alv.pub:9292
    openstack endpoint create --region RegionOne image admin http://glance1.alv.pub:9292




nova控制节点
`````````````````

创建Nova数据库、用户、认证，


.. code-block:: bash

    source ./admin-openstack.sh
    openstack service create --name nova --description "OpenStack Compute" compute
    openstack endpoint create --region RegionOne compute public http://controller.alv.pub:8774/v2.1
    openstack endpoint create --region RegionOne compute internal http://controller.alv.pub:8774/v2.1
    openstack endpoint create --region RegionOne compute admin http://controller.alv.pub:8774/v2.1


创建placement用户、服务、API

.. code-block:: bash

    openstack user create --domain default --password=placement placement
    openstack role add --project service --user placement admin
    openstack service create --name placement --description "Placement API" placement
    openstack endpoint create --region RegionOne placement public http://controller.alv.pub:8778
    openstack endpoint create --region RegionOne placement internal http://controller.alv.pub:8778
    openstack endpoint create --region RegionOne placement admin http://controller.alv.pub:8778
    #openstack endpoint delete id?


安装nova控制节点
----------------------------------------------

.. code-block:: bash

    yum install -y openstack-nova-api openstack-nova-conductor \
      openstack-nova-console openstack-nova-novncproxy \
      openstack-nova-scheduler openstack-nova-placement-api


nova控制节点配置
----------------------------------------------

.. code-block:: bash


    echo '#
    [DEFAULT]
    enabled_apis = osapi_compute,metadata
    transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub
    my_ip = 192.168.127.88
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
    memcached_servers = memcached.alv.pub:11211
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    project_name = service
    username = nova
    password = nova

    [vnc]
    enabled = true
    vncserver_listen = $my_ip
    vncserver_proxyclient_address = $my_ip
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

    [scheduler]
    discover_hosts_in_cells_interval = 300
    #'>/etc/nova/nova.conf



.. code-block:: bash

    echo "

    #Placement API
    <Directory /usr/bin>
       <IfVersion >= 2.4>
          Require all granted
       </IfVersion>
       <IfVersion < 2.4>
          Order allow,deny
          Allow from all
       </IfVersion>
    </Directory>
    ">>/etc/httpd/conf.d/00-nova-placement-api.conf

.. code-block:: bash

    systemctl restart httpd


同步数据库
-----------------------

.. code-block:: bash


    su -s /bin/sh -c "nova-manage api_db sync" nova
    su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
    su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
    su -s /bin/sh -c "nova-manage db sync" nova


检测数据

.. code-block:: bash


    nova-manage cell_v2 list_cells

    mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova_api;show tables;"
    mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova;show tables;"
    mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova_cell0;show tables;"

开机自启动
-----------------------

.. code-block:: bash

    systemctl enable openstack-nova-api.service \
    openstack-nova-consoleauth.service openstack-nova-scheduler.service \
    openstack-nova-conductor.service openstack-nova-novncproxy.service


启动服务
-----------------------

.. code-block:: bash

    systemctl start openstack-nova-api.service \
      openstack-nova-consoleauth.service openstack-nova-scheduler.service \
      openstack-nova-conductor.service openstack-nova-novncproxy.service

查看节点
-----------------------

.. code-block:: bash

    #nova service-list
    openstack catalog list
    nova-status upgrade check
    openstack compute service list

Neutron Deployment
```````````````````````````

 本实例网络配置方式是：公共网络

 官方参考 https://docs.openstack.org/neutron/pike/install/controller-install-rdo.html

 创建Neutron数据库、用户认证，前面已设置




创建Neutron服务实体,API端点
----------------------------------------------

.. code-block:: bash

    openstack service create --name neutron --description "OpenStack Networking" network
    openstack endpoint create --region RegionOne network public http://controller.alv.pub:9696
    openstack endpoint create --region RegionOne network internal http://controller.alv.pub:9696
    openstack endpoint create --region RegionOne network admin http://controller.alv.pub:9696


安装软件
-----------------------

.. code-block:: bash

    #wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
    #yum install centos-release-openstack-pike -y #安装OpenStack库
    #sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
    yum install -y openstack-neutron openstack-neutron-ml2 \
    openstack-neutron-linuxbridge python-neutronclient ebtables ipset

Neutron 备份配置
-----------------------

.. code-block:: bash

    cp /etc/neutron/neutron.conf{,.bak2}
    cp /etc/neutron/plugins/ml2/ml2_conf.ini{,.bak}
    ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
    cp /etc/neutron/plugins/ml2/linuxbridge_agent.ini{,.bak}
    cp /etc/neutron/dhcp_agent.ini{,.bak}
    cp /etc/neutron/metadata_agent.ini{,.bak}
    cp /etc/neutron/l3_agent.ini{,.bak}

配置

.. code-block:: bash

    echo '
    [DEFAULT]
    nova_metadata_ip = nova1.alv.pub
    metadata_proxy_shared_secret = metadata
    #'>/etc/neutron/metadata_agent.ini

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
    service_metadata_proxy = true
    metadata_proxy_shared_secret = metadata
    #'>>/etc/nova/nova.conf

.. code-block:: bash

    echo '#
    [ml2]
    tenant_network_types =
    type_drivers = vlan,flat
    mechanism_drivers = linuxbridge
    extension_drivers = port_security
    [ml2_type_flat]
    flat_networks = provider
    [securitygroup]
    enable_ipset = True
    #vlan
    # [ml2_type_valn]
    # network_vlan_ranges = provider:3001:4000
    #'>/etc/neutron/plugins/ml2/ml2_conf.ini

# ens32是网卡名

.. code-block:: bash

    echo '#
    [linux_bridge]
    physical_interface_mappings = provider:ens32
    [vxlan]
    enable_vxlan = false
    #local_ip = 10.2.1.20
    #l2_population = true
    [agent]
    prevent_arp_spoofing = True
    [securitygroup]
    firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
    enable_security_group = True
    #'>/etc/neutron/plugins/ml2/linuxbridge_agent.ini

.. code-block:: bash

    echo '#
    [DEFAULT]
    interface_driver = linuxbridge
    dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
    enable_isolated_metadata = true
    #'>/etc/neutron/dhcp_agent.ini


.. code-block:: bash

    echo '
    [DEFAULT]
    core_plugin = ml2
    service_plugins = router
    allow_overlapping_ips = true
    transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub
    auth_strategy = keystone
    notify_nova_on_port_status_changes = true
    notify_nova_on_port_data_changes = true

    [keystone_authtoken]
    auth_uri = http://keystone1.alv.pub:5000
    auth_url = http://keystone1.alv.pub:35357
    memcached_servers = memcached.alv.pub:11211
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    project_name = service
    username = neutron
    password = neutron

    [nova]
    auth_url = http://keystone1.alv.pub:35357
    auth_type = password
    project_domain_id = default
    user_domain_id = default
    region_name = RegionOne
    project_name = service
    username = nova
    password = nova

    [database]
    connection = mysql://neutron:neutron@maxscale.alv.pub:4006/neutron

    [oslo_concurrency]
    lock_path = /var/lib/neutron/tmp
    #'>/etc/neutron/neutron.conf

.. code-block:: bash

    echo '
    [DEFAULT]
    interface_driver = linuxbridge
    #'>/etc/neutron/l3_agent.ini


同步数据库
-----------------------

.. code-block:: bash

    su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron

检测数据

.. code-block:: bash

    mysql -h maxscale.alv.pub -P4006 -u neutron -pneutron -e "use neutron;show tables;"



重启相关服务
-----------------------

.. code-block:: bash

    systemctl restart openstack-nova-api.service



启动neutron
-----------------------

.. code-block:: bash

    systemctl enable neutron-server.service \
      neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
      neutron-metadata-agent.service neutron-l3-agent
    systemctl start neutron-server.service \
      neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
      neutron-metadata-agent.service neutron-l3-agent
    echo "查看网络,正常是：控制节点3个ID"


 openstack 客户端执行

.. code-block:: bash

    openstack network agent list







安装配置horizon
```````````````````````````

安装软件
-----------------------

.. code-block:: bash

    yum install openstack-dashboard python-memcached -y


配置
-----------------------

.. code-block:: bash

    cp /etc/openstack-dashboard/local_settings{,.bak}
    #egrep -v '#|^$' /etc/openstack-dashboard/local_settings #显示默认配置
    Setfiles=/etc/openstack-dashboard/local_settings
    sed -i 's#_member_#user#g' $Setfiles
    sed -i 's#OPENSTACK_HOST = "127.0.0.1"#OPENSTACK_HOST = "keystone1.alv.pub"#' $Setfiles
    ##允许所有主机访问#
    sed -i "/ALLOWED_HOSTS/cALLOWED_HOSTS = ['*', ]" $Setfiles
    #去掉memcached注释#
    sed -in '153,158s/#//' $Setfiles
    sed -in '160,164s/.*/#&/' $Setfiles
    sed -i 's#UTC#Asia/Shanghai#g' $Setfiles
    sed -i 's#%s:5000/v2.0#%s:5000/v3#' $Setfiles

 sed -i '/MULTIDOMAIN_SUPPORT/cOPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False' $Setfiles
    sed -i "s@^#OPENSTACK_KEYSTONE_DEFAULT@OPENSTACK_KEYSTONE_DEFAULT@" $Setfiles


.. code-block:: bash

    echo '
    #set
    OPENSTACK_API_VERSIONS = {
        "identity": 3,
        "image": 2,
        "volume": 2,
    }
    #'>>$Setfiles

登录界面域
-----------------------

 设置为默认域，default， 进行该设置后，登录页面不再有domain输入框

.. code-block:: bash

    sed -i '/MULTIDOMAIN_SUPPORT/cOPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False' /etc/openstack-dashboard/local_settings

.. code-block:: bash

    systemctl enable httpd
    systemctl restart httpd

cinder块存储控制节点
`````````````````````````````

 #存储节点安装配置cinder-volume服务
 #控制节点安装配置cinder-api、cinder-scheduler服务




keystone创建cinder用户、服务、API
----------------------------------------------
 #以下操纵在openstack客户端做，这里我们是在horizon.alv.pub上执行的。

.. code-block:: bash

    source ./admin-openstack.sh
    openstack user create --domain default --password=cinder cinder
    openstack role add --project service --user cinder admin
    openstack service create --name cinderv2   --description "OpenStack Block Storage" volumev2
    openstack service create --name cinderv3   --description "OpenStack Block Storage" volumev3
    openstack endpoint create --region RegionOne   volumev2 public http://controller.alv.pub:8776/v2/%\(project_id\)s
    openstack endpoint create --region RegionOne   volumev2 internal http://controller.alv.pub:8776/v2/%\(project_id\)s
    openstack endpoint create --region RegionOne   volumev2 admin http://controller.alv.pub:8776/v2/%\(project_id\)s
    openstack endpoint create --region RegionOne   volumev3 public http://controller.alv.pub:8776/v3/%\(project_id\)s
    openstack endpoint create --region RegionOne   volumev3 internal http://controller.alv.pub:8776/v3/%\(project_id\)s
    openstack endpoint create --region RegionOne   volumev3 admin http://controller.alv.pub:8776/v3/%\(project_id\)s




安装软件并备份配置文件
----------------------------------------------

.. code-block:: bash

    yum install openstack-cinder python-memcached -y
    yum install nfs-utils -y #NFS
    cp /etc/cinder/cinder.conf{,.bak}



创建数据库和用户
----------------------------------------------
 该操作我们是在maxscale.alv.pub:4006 数据库里做的。



配置cinder
----------------------------------------------

.. code-block:: bash

    echo '
    [DEFAULT]
    auth_strategy = keystone
    log_dir = /var/log/cinder
    state_path = /var/lib/cinder
    glance_api_servers = http://glance1.alv.pub:9292
    transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub

    [database]
    connection = mysql+pymysql://cinder:cinder@maxscale.alv.pub:4006/cinder

    [keystone_authtoken]
    auth_uri = http://keystone1.alv.pub:5000
    auth_url = http://keystone1.alv.pub:35357
    memcached_servers = memcached.alv.pub:11211
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    project_name = service
    username = cinder
    password = cinder

    [oslo_concurrency]
    lock_path = /var/lib/cinder/tmp
    '>/etc/cinder/cinder.conf


在nova控制节点添加配置
----------------------------------------------

.. code-block:: bash

    echo '
    [cinder]
    os_region_name = RegionOne
    '>>/etc/nova/nova.conf


重启服务
-----------------------

.. code-block:: bash

    systemctl restart openstack-nova-api.service

初始化数据
-----------------------

.. code-block:: bash

    su -s /bin/sh -c "cinder-manage db sync" cinder
    mysql -hmaxscale -u cinder -pcinder -P4006 -e "use cinder;show tables;" #检测


启动cinder服务
-----------------------

.. code-block:: bash

    systemctl enable openstack-cinder-api.service openstack-cinder-scheduler.service
    systemctl start openstack-cinder-api.service openstack-cinder-scheduler.service
    netstat -antp|grep 8776 #cheack

.. code-block:: bash

    cinder service-list






