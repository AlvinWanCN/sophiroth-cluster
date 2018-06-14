################################
controller.alv.pub
################################


.. contents::

添加openstack的仓库
```````````````````````
.. code-block:: bash

    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo



Keystone安装
```````````````````
.. code-block:: bash

    yum install -y openstack-keystone httpd mod_wsgi memcached python-memcached
    yum install apr apr-util -y

memcached启动和设置
```````````````````
.. code-block:: bash

    cp /etc/sysconfig/memcached{,.bak}
    systemctl enable memcached.service
    systemctl start memcached.service
    netstat -antp|grep 11211



Keystone 配置
```````````````````
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
servers = controller.alv.pub:11211
">/etc/keystone/keystone.conf



## 初始化身份认证服务的数据库
```
su -s /bin/sh -c "keystone-manage db_sync" keystone
```

### 检查表是否创建成功
```
mysql -ukeystone -pkeystone -hmaxscale.alv.pub -P4006 -e "use keystone;show tables;"
```

## 初始化密钥存储库

```
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
```

## 设置admin用户（管理用户）和密码


keystone-manage bootstrap --bootstrap-password admin \
  --bootstrap-admin-url http://controller.alv.pub:35357/v3/ \
  --bootstrap-internal-url http://controller.alv.pub:5000/v3/ \
  --bootstrap-public-url http://controller.alv.pub:5000/v3/ \
  --bootstrap-region-id RegionOne


## apache配置

```
cp /etc/httpd/conf/httpd.conf{,.bak}
echo "ServerName controller.alv.pub">>/etc/httpd/conf/httpd.conf
ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/

Apache HTTP 启动并设置开机自启动
```````````````````````````````````

systemctl enable httpd.service
systemctl restart httpd.service
netstat -antp|egrep ':5000|:35357|:80'


## 创建 OpenStack 客户端环境脚本

以下操作是在openstack客户端做的，这里我们是在horizon.alv.pub上做的。

```
echo "
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_AUTH_URL=http://controller.alv.pub:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
">./admin-openstack.sh
```

### 测试脚本是否生效

```
source ./admin-openstack.sh
yum install python-openstackclient openstack-selinux python2-PyMySQL -y #OpenStack客户端
yum install openstack-utils -y #openstack工具
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
export OS_AUTH_URL=http://controller.alv.pub:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
">./demo-openstack.sh
```

### 测试脚本是否生效
```
source ./demo-openstack.sh
openstack token issue
```

安装配置glance
```````````````````



## 创建Glance数据库、用户、认证，前面已设置
在数据库openstack使用的数据库离设置，这里我们设置在maxscale.alv.pub里。

```
create database glance;
grant all privileges on glance.* to 'glance'@'localhost' identified by 'glance';
grant all privileges on glance.* to 'glance'@'%' identified by 'glance';
```

## keystone上服务注册 ,创建glance服务实体,API端点（公有、私有、admin）

这个操作在openstack客户端做。
这里我是在horizon.alv.pub上做的下面操作。
```
source ./admin-openstack.sh || { echo "加载前面设置的admin-openstack.sh环境变量脚本";exit; }
openstack service create --name glance --description "OpenStack Image" image
openstack endpoint create --region RegionOne image public http://controller.alv.pub:9292
openstack endpoint create --region RegionOne image internal http://controller.alv.pub:9292
openstack endpoint create --region RegionOne image admin http://controller.alv.pub:9292

```

## Install Glance
回到controller.alv.pub上操作。
```
sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
yum install openstack-glance python-glance python-memcached -y

```

## 配置

```
cp /etc/glance/glance-api.conf{,.bak}
cp /etc/glance/glance-registry.conf{,.bak}
```

#images默认/var/lib/glance/images/

```
Imgdir=/XLH_DATE/images
mkdir -p $Imgdir
chown glance:nobody $Imgdir
echo "镜像目录： $Imgdir"
echo "#
[database]
connection = mysql+pymysql://glance:glance@maxscale.alv.pub:4006/glance
[keystone_authtoken]
auth_uri = http://controller.alv.pub:5000/v3
auth_url = http://controller.alv.pub:35357/v3
memcached_servers = controller.alv.pub:11211
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

#

echo "#
[database]
connection = mysql+pymysql://glance:glance@maxscale.alv.pub:4006/glance
[keystone_authtoken]
auth_uri = http://controller.alv.pub:5000/v3
auth_url = http://controller.alv.pub:35357/v3
memcached_servers = controller.alv.pub:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = glance
password = glance
[paste_deploy]
flavor = keystone
#">/etc/glance/glance-registry.conf
```

## 同步数据库,检查数据库

```
su -s /bin/sh -c "glance-manage db_sync" glance
mysql -h maxscale.alv.pub -u glance -pglance -P4006 -e "use glance;show tables;"
```

## 启动服务并设置开机自启动

```
systemctl enable openstack-glance-api openstack-glance-registry
systemctl start openstack-glance-api openstack-glance-registry
#systemctl restart openstack-glance-api  openstack-glance-registry
netstat -antp|egrep '9292|9191' #检测服务端口
```

## 镜像测试,下载有时很慢

wget http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img #下载测试镜像源


#使用qcow2磁盘格式，bare容器格式,上传镜像到镜像服务并设置公共可见

```
source ./admin-openstack.sh


openstack image create "cirros" \
  --file cirros-0.3.5-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --public
#检查是否上传成功
openstack image list
#glance image-list
ls $Imgdir

#删除镜像 glance image-delete 镜像id
```