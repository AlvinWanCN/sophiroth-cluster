
<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

# cinder块存储控制节点

#存储节点安装配置cinder-volume服务
#控制节点安装配置cinder-api、cinder-scheduler服务


### 添加OpenStack的仓库

```
curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/TechnologyCenter/master/linux/software/yum.repos.d/openstack_pick_centos7.repo > /etc/yum.repos.d/openstack_pick_centos7.repo
```



### 安装软件并备份配置文件

```

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
glance_api_servers = http://glance.alv.pub:9292
transport_url = rabbit://openstack:openstack@rabbitmq1.alv.pub

[database]
connection = mysql+pymysql://cinder:cinder@maxscale.alv.pub:4006/cinder

[keystone_authtoken]
auth_uri = http://keystone1.alv.pub:5000
auth_url = http://keystone1.alv.pub:35357
memcached_servers = keystone1.alv.pub:11211
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
