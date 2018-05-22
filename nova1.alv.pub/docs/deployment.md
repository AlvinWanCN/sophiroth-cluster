

# nova控制节点

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
openstack endpoint create --region RegionOne compute public http://nova1.alv.pub:8774/v2.1
openstack endpoint create --region RegionOne compute internal http://nova1.alv.pub:8774/v2.1
openstack endpoint create --region RegionOne compute admin http://nova1.alv.pub:8774/v2.1

```

### 创建placement用户、服务、API
```
openstack user create --domain default --password=placement placement
openstack role add --project service --user placement admin
openstack service create --name placement --description "Placement API" placement
openstack endpoint create --region RegionOne placement public http://nova1.alv.pub:8778
openstack endpoint create --region RegionOne placement internal http://nova1.alv.pub:8778
openstack endpoint create --region RegionOne placement admin http://nova1.alv.pub:8778
#openstack endpoint delete id?
```

## 安装nova控制节点

```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum install centos-release-openstack-pike -y #安装OpenStack库
mv /etc/yum.repos.d/CentOS-QEMU-EV.repo /tmp/
yum install -y openstack-nova-api openstack-nova-conductor \
  openstack-nova-console openstack-nova-novncproxy \
  openstack-nova-scheduler openstack-nova-placement-api
yum install -y openstack-utils
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
auth_uri = http://keystone1.alv.pub:5000
auth_url = http://keystone1.alv.pub:35357
memcached_servers = keystone1.alv.pub:11211
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
api_servers = http://glance.alv.pub:9292
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

```
nova-manage cell_v2 list_cells
```

```
mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova_api;show tables;"
mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova;show tables;"
mysql -h maxscale.alv.pub -u nova -pnova -P4006 -e "use nova_cell0;show tables;"
```

## 开机自启动
```
 systemctl enable openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service
```

## 启动服务

```
systemctl start openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service
```

## 查看节点

```
#nova service-list
openstack catalog list
nova-status upgrade check
openstack compute service list

```