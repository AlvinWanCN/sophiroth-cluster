glance1.alv.pub
##########################


.. contents::

Install Glance
----------------------------------------------


添加openstack的仓库
-------------------
.. code-block:: bash

    python -c "$(curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/scripts/master/common_tools/pullLocalYum.py)" #add local basic repository
    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo


.. code-block:: bash

    sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
    yum install openstack-glance python-glance python-memcached -y


配置Glance
-----------------------

.. code-block:: bash

    cp /etc/glance/glance-api.conf{,.bak}
    cp /etc/glance/glance-registry.conf{,.bak}


 images默认/var/lib/glance/images/

.. code-block:: bash

    Imgdir=/data/images
    mkdir -p $Imgdir
    chown glance:nobody $Imgdir
    echo "镜像目录： $Imgdir"
    echo "#
    [database]
    connection = mysql+pymysql://glance:glance@maxscale.alv.pub:4006/glance
    [keystone_authtoken]
    auth_uri = http://keystone1.alv.pub:5000/v3
    auth_url = http://keystone1.alv.pub:35357/v3
    memcached_servers = memcached.alv.pub:11211
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    project_name = service
    username = glance
    password = glance
    [paste_deploy]
    flavor = keystone
    [glance_store]
    stores = file,http
    default_store = file
    filesystem_store_datadir = $Imgdir
    #">/etc/glance/glance-api.conf

.. code-block:: bash

    echo "#
    [database]
    connection = mysql+pymysql://glance:glance@maxscale.alv.pub:4006/glance
    [keystone_authtoken]
    auth_uri = http://keystone1.alv.pub:5000/v3
    auth_url = http://keystone1.alv.pub:35357/v3
    memcached_servers = memcached.alv.pub:11211
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    project_name = service
    username = glance
    password = glance
    [paste_deploy]
    flavor = keystone
    #">/etc/glance/glance-registry.conf


同步数据库,检查数据库
----------------------------------------------
.. code-block:: bash

    su -s /bin/sh -c "glance-manage db_sync" glance
    mysql -h maxscale.alv.pub -u glance -pglance -P4006 -e "use glance;show tables;"


启动服务并设置开机自启动
----------------------------------------------
.. code-block:: bash

    systemctl enable openstack-glance-api openstack-glance-registry
    systemctl start openstack-glance-api openstack-glance-registry
    #systemctl restart openstack-glance-api  openstack-glance-registry
    netstat -antp|egrep '9292|9191' #检测服务端口


镜像测试,下载有时很慢
----------------------------------------------

.. code-block:: bash

    #wget http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img #下载测试镜像源
    wget http://dc.alv.pub/openstack_pick_centos7/cirros-0.3.5-x86_64-disk.img


使用qcow2磁盘格式，bare容器格式,上传镜像到镜像服务并设置公共可见
---------------------------------------------------------------------

.. code-block:: bash

    source ./admin-openstack.sh

    openstack image create "cirros" \
      --file cirros-0.3.5-x86_64-disk.img \
      --disk-format qcow2 --container-format bare \
      --public

检查是否上传成功
----------------------------------------------

.. code-block:: bash

    openstack image list
    #glance image-list
    ls $Imgdir

 #删除镜像 glance image-delete 镜像id