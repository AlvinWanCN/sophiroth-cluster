################################
controller.alv.pub
################################


.. contents::

添加openstack的仓库
```````````````````````
.. code-block:: bash

    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo

创建相应的数据库
``````````````````````

.. code-block:: mysql

    create database keystone;
    grant all privileges on keystone.* to 'keystone'@'localhost' identified by 'keystone';
    grant all privileges on keystone.* to 'keystone'@'%' identified by 'keystone';
    create database glance;
    grant all privileges on glance.* to 'glance'@'localhost' identified by 'glance';
    grant all privileges on glance.* to 'glance'@'%' identified by 'glance';

    create database nova;
    grant all privileges on nova.* to 'nova'@'localhost' identified by 'nova';
    grant all privileges on nova.* to 'nova'@'%' identified by 'nova';
    create database nova_api;
    grant all privileges on nova_api.* to 'nova'@'localhost' identified by 'nova';
    grant all privileges on nova_api.* to 'nova'@'%' identified by 'nova';
    create database nova_cell0;
    grant all privileges on nova_cell0.* to 'nova'@'localhost' identified by 'nova';
    grant all privileges on nova_cell0.* to 'nova'@'%' identified by 'nova';

    create database neutron;
    grant all privileges on neutron.* to 'neutron'@'localhost' identified by 'neutron';
    grant all privileges on neutron.* to 'neutron'@'%' identified by 'neutron';

    create database cinder;
    grant all privileges on cinder.* to 'cinder'@'localhost' identified by 'cinder';
    grant all privileges on cinder.* to 'cinder'@'%' identified by 'cinder';

    flush privileges;
    select user,host from mysql.user;
    show databases;

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

创建demo项目(普通用户密码及角色)


openstack project create --domain default --description "Demo Project" demo
openstack user create --domain default --password=demo demo
openstack role create user
openstack role add --project demo --user demo user


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





nova控制节点
`````````````````

## 创建Nova数据库、用户、认证，

以下数据库操作在maxscle.alv.pub里做的
```
create database nova;
grant all privileges on nova.* to 'nova'@'localhost' identified by 'nova';
grant all privileges on nova.* to 'nova'@'%' identified by 'nova';

```


## keystone上服务注册 ,创建nova用户、服务、API
以下操作在openstack客户端执行，这里我们在horizon.alv.pub上执行

#nova用户前面已建,在安装好keystone的时候创建的。
```
source ./admin-openstack.sh
openstack service create --name nova --description "OpenStack Compute" compute
openstack endpoint create --region RegionOne compute public http://controller.alv.pub:8774/v2.1
openstack endpoint create --region RegionOne compute internal http://controller.alv.pub:8774/v2.1
openstack endpoint create --region RegionOne compute admin http://controller.alv.pub:8774/v2.1

```

### 创建placement用户、服务、API
```
openstack user create --domain default --password=placement placement
openstack role add --project service --user placement admin
openstack service create --name placement --description "Placement API" placement
openstack endpoint create --region RegionOne placement public http://controller.alv.pub:8778
openstack endpoint create --region RegionOne placement internal http://controller.alv.pub:8778
openstack endpoint create --region RegionOne placement admin http://controller.alv.pub:8778
#openstack endpoint delete id?
```

## 安装nova控制节点

```
yum install -y openstack-nova-api openstack-nova-conductor \
  openstack-nova-console openstack-nova-novncproxy \
  openstack-nova-scheduler openstack-nova-placement-api
```

## nova控制节点配置

```
echo '#
[DEFAULT]
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
auth_uri = http://controller.alv.pub:5000
auth_url = http://controller.alv.pub:35357
memcached_servers = controller.alv.pub:11211
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
api_servers = http://controller.alv.pub:9292
[oslo_concurrency]
lock_path = /var/lib/nova/tmp

[placement]
os_region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller.alv.pub:35357/v3
username = placement
password = placement

[scheduler]
discover_hosts_in_cells_interval = 300
#'>/etc/nova/nova.conf
```


```

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

```

```
systemctl restart httpd
sleep 2
```

## 同步数据库

```
su -s /bin/sh -c "nova-manage api_db sync" nova
su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
su -s /bin/sh -c "nova-manage db sync" nova
```

## 检测数据


nova-manage cell_v2 list_cells

mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova_api;show tables;"
mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova;show tables;"
mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova_cell0;show tables;"
```

## 开机自启动

 systemctl enable openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service


## 启动服务


systemctl start openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service

## 查看节点

```
#nova service-list
openstack catalog list
nova-status upgrade check
openstack compute service list

```







# Neutron Deployment

#本实例网络配置方式是：公共网络

#官方参考 https://docs.openstack.org/neutron/pike/install/controller-install-rdo.html

## 创建Neutron数据库、用户认证，前面已设置

### 在数据库里的配置
这里我们是在maxscale.alv.pub里做以下操作
```
create database neutron;
grant all privileges on neutron.* to 'neutron'@'localhost' identified by 'neutron';
grant all privileges on neutron.* to 'neutron'@'%' identified by 'neutron';
```


## 创建Neutron服务实体,API端点
这里我们在openstack客户端做以下配置，这里我们在horizon.alv.pub配置这些。

```
openstack service create --name neutron --description "OpenStack Networking" network
openstack endpoint create --region RegionOne network public http://controller.alv.pub:9696
openstack endpoint create --region RegionOne network internal http://controller.alv.pub:9696
openstack endpoint create --region RegionOne network admin http://controller.alv.pub:9696
```

## 安装软件

```
#wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
#yum install centos-release-openstack-pike -y #安装OpenStack库
#sed -i 's/\$contentdir/centos-7/' /etc/yum.repos.d/CentOS-QEMU-EV.repo
yum install -y openstack-neutron openstack-neutron-ml2 \
openstack-neutron-linuxbridge python-neutronclient ebtables ipset
```

## Neutron 备份配置
```
cp /etc/neutron/neutron.conf{,.bak2}
cp /etc/neutron/plugins/ml2/ml2_conf.ini{,.bak}
ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
cp /etc/neutron/plugins/ml2/linuxbridge_agent.ini{,.bak}
cp /etc/neutron/dhcp_agent.ini{,.bak}
cp /etc/neutron/metadata_agent.ini{,.bak}
cp /etc/neutron/l3_agent.ini{,.bak}
```

## 配置
```
echo '
[DEFAULT]
nova_metadata_ip = nova1.alv.pub
metadata_proxy_shared_secret = metadata
#'>/etc/neutron/metadata_agent.ini
#
echo '
#
[neutron]
url = http://controller.alv.pub:9696
auth_url = http://controller.alv.pub:35357
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
#
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
# bond0是网卡名
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
#
echo '#
[DEFAULT]
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true
#'>/etc/neutron/dhcp_agent.ini
#
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
auth_uri = http://controller.alv.pub:5000
auth_url = http://controller.alv.pub:35357
memcached_servers = controller.alv.pub:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = neutron

[nova]
auth_url = http://controller.alv.pub:35357
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
#
echo '
[DEFAULT]
interface_driver = linuxbridge
#'>/etc/neutron/l3_agent.ini
```

## 同步数据库
```
su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
```
## 检测数据


```
mysql -h maxscale.alv.pub -P4006 -u neutron -pneutron -e "use neutron;show tables;"

```

## 重启相关服务


```
systemctl restart openstack-nova-api.service

```

## 启动neutron
```
systemctl enable neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service neutron-l3-agent
systemctl start neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service neutron-l3-agent
echo "查看网络,正常是：控制节点3个ID"

```

openstack 客户端执行
```
openstack network agent list
```




# Deployments
该服务器上我们主要是用于两个用途，一是openstack客户端，二是Dashboard web管理界面，这里的Dashboard我使用horizone

##下面我们是先安装openstack客户端

### 更换阿里云

```



### 创建 OpenStack 客户端环境脚本


#### 测试脚本是否生效








## 安装配置horizon

### 安装软件

```
yum install openstack-dashboard python-memcached -y
```

### 配置

```
cp /etc/openstack-dashboard/local_settings{,.bak}
#egrep -v '#|^$' /etc/openstack-dashboard/local_settings #显示默认配置
Setfiles=/etc/openstack-dashboard/local_settings
sed -i 's#_member_#user#g' $Setfiles
sed -i 's#OPENSTACK_HOST = "127.0.0.1"#OPENSTACK_HOST = "controller.alv.pub"#' $Setfiles
##允许所有主机访问#
sed -i "/ALLOWED_HOSTS/cALLOWED_HOSTS = ['*', ]" $Setfiles
#去掉memcached注释#
sed -in '153,158s/#//' $Setfiles
sed -in '160,164s/.*/#&/' $Setfiles
sed -i 's#UTC#Asia/Shanghai#g' $Setfiles
sed -i 's#%s:5000/v2.0#%s:5000/v3#' $Setfiles

sed -i '/ULTIDOMAIN_SUPPORT/cOPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True' $Setfiles
sed -i "s@^#OPENSTACK_KEYSTONE_DEFAULT@OPENSTACK_KEYSTONE_DEFAULT@" $Setfiles
```

```
echo '
#set
OPENSTACK_API_VERSIONS = {
    "identity": 3,
    "image": 2,
    "volume": 2,
}
#'>>$Setfiles
#
```
####登录界面域
设置为默认域，default， 进行该设置后，登录页面不再有domain输入框
```
sed -i '/MULTIDOMAIN_SUPPORT/cOPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False' /etc/openstack-dashboard/local_settings
```

```
systemctl enable httpd
systemctl restart httpd
```












