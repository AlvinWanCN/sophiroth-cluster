
<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

# cinder块存储控制节点

#存储节点安装配置cinder-volume服务
#控制节点安装配置cinder-api、cinder-scheduler服务


### 添加OpenStack的仓库

```
curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo
```

### keystone创建cinder用户、服务、API
以下操纵在openstack客户端做，这里我们是在horizon.alv.pub上执行的。
```
source ./admin-openstack.sh
openstack user create --domain default --password=cinder cinder
openstack role add --project service --user cinder admin
openstack service create --name cinderv2   --description "OpenStack Block Storage" volumev2
openstack service create --name cinderv3   --description "OpenStack Block Storage" volumev3
openstack endpoint create --region RegionOne   volumev2 public http://cinder-control1.alv.pub:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne   volumev2 internal http://cinder-control1.alv.pub:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne   volumev2 admin http://cinder-control1.alv.pub:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne   volumev3 public http://cinder-control1.alv.pub:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne   volumev3 internal http://cinder-control1.alv.pub:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne   volumev3 admin http://cinder-control1.alv.pub:8776/v3/%\(project_id\)s

```


### 安装软件并备份配置文件

```
yum install openstack-cinder python-memcached -y
yum install nfs-utils -y #NFS
cp /etc/cinder/cinder.conf{,.bak}
```


### 创建数据库和用户
该操作我们是在maxscale.alv.pub:4006 数据库里做的。

```
create database cinder;
grant all privileges on cinder.* to 'cinder'@'localhost' identified by 'cinder';
grant all privileges on cinder.* to 'cinder'@'%' identified by 'cinder';
flush privileges;
```


### 配置cinder
```
echo '
[DEFAULT]
auth_strategy = keystone
log_dir = /var/log/cinder
state_path = /var/lib/cinder
glance_api_servers = http://controller.alv.pub:9292
transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub

[database]
connection = mysql+pymysql://cinder:cinder@maxscale.alv.pub:4006/cinder

[keystone_authtoken]
auth_uri = http://controller.alv.pub:5000
auth_url = http://controller.alv.pub:35357
memcached_servers = controller.alv.pub:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = cinder
password = cinder

[oslo_concurrency]
lock_path = /var/lib/cinder/tmp
'>/etc/cinder/cinder.conf
```

### 在nova控制节点添加配置


```
echo '
[cinder]
os_region_name = RegionOne
'>>/etc/nova/nova.conf

```
然后重启服务

```
systemctl restart openstack-nova-api.service
```

### 初始化数据

```
su -s /bin/sh -c "cinder-manage db sync" cinder
mysql -hmaxscale -u cinder -pcinder -P4006 -e "use cinder;show tables;" #检测

```m

### 启动cinder服务

```
systemctl enable openstack-cinder-api.service openstack-cinder-scheduler.service
systemctl start openstack-cinder-api.service openstack-cinder-scheduler.service
netstat -antp|grep 8776 #cheack

```

cinder service-list