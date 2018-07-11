
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


然后去openstack客户端做操作

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
```

### 测试脚本是否生效

```
source ./admin-openstack.sh
openstack token issue
```

### 创建service项目,创建glance,nova,neutron用户，并授权

```
openstack project create --domain default --description "Service Project" service
openstack user create --domain default --password=glance glance
openstack role add --project service --user glance admin
openstack user create --domain default --password=nova nova
openstack role add --project service --user nova admin
openstack user create --domain default --password=neutron neutron
openstack role add --project service --user neutron admin
```

### 创建demo项目(普通用户密码及角色)

```
openstack project create --domain default --description "Demo Project" demo
openstack user create --domain default --password=demo demo
openstack role create user
openstack role add --project demo --user demo user
```

### demo环境脚本

```
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
```

### 测试脚本是否生效
```
source ./demo-openstack.sh
yum install python-openstackclient openstack-selinux python2-PyMySQL -y #OpenStack客户端
openstack token issue
openstack token issue
```