
keystone.alv.pub
########################

.. contents::

添加openstack的仓库
-------------------
.. code-block:: bash

    mv /etc/yum.repos.d/* /tmp/
    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/centos7.dc.alv.pub.repo > /etc/yum.repos.d/centos7.dc.alv.pub.repo
    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/epel.dc.alv.pub.repo > /etc/yum.repos.d/epel.dc.alv.pub.repo
    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/tech-center/master/software/yum.repos.d/queens.repo > /etc/yum.repos.d/queens.repo

安装keystone
-------------------

.. code-block:: bash

    yum install -y openstack-keystone httpd mod_wsgi memcached python-memcached
    yum install apr apr-util -y


Keystone 配置
-----------------------

.. code-block:: bash

    cp /etc/keystone/keystone.conf{,.bak}  #备份默认配置
    Keys=$(openssl rand -hex 10)  #生成随机密码
    echo $Keys
    echo "kestone  $Keys">>~/openstack.log
    echo "
    [DEFAULT]
    admin_token = $Keys
    verbose = true
    [database]
    connection = mysql+pymysql://keystone:keystone@maxscale.alv.pub:4006/keystone
    [token]
    provider = fernet
    driver = memcache
    [memcache]
    servers =  memcached.alv.pub:11211
    ">/etc/keystone/keystone.conf



初始化身份认证服务的数据库
-----------------------

.. code-block:: bash

    su -s /bin/sh -c "keystone-manage db_sync" keystone


 检查表是否创建成功
.. code-block:: bash

    mysql -ukeystone -pkeystone -hmaxscale.alv.pub -P4006 -e "use keystone;show tables;"


初始化密钥存储库
-----------------------

.. code-block:: bash

    keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
    keystone-manage credential_setup --keystone-user keystone --keystone-group keystone


设置admin用户（管理用户）和密码
----------------------------------------------

.. code-block:: bash

    keystone-manage bootstrap --bootstrap-password admin \
      --bootstrap-admin-url http://keystone1.alv.pub:35357/v3/ \
      --bootstrap-internal-url http://keystone1.alv.pub:5000/v3/ \
      --bootstrap-public-url http://keystone1.alv.pub:5000/v3/ \
      --bootstrap-region-id RegionOne


apache配置
-----------------------

.. code-block:: bash

    cp /etc/httpd/conf/httpd.conf{,.bak}
    echo "ServerName keystone1.alv.pub">>/etc/httpd/conf/httpd.conf
    ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/

Apache HTTP 启动并设置开机自启动
----------------------------------------------

.. code-block:: bash

    systemctl enable httpd.service
    systemctl restart httpd.service
    netstat -antp|egrep ':5000|:35357|:80'
