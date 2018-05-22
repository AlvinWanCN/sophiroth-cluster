<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


# glance server

this is glance server, and also is openstack server.

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
openstack endpoint create --region RegionOne image public http://glance.alv.pub:9292
openstack endpoint create --region RegionOne image internal http://glance.alv.pub:9292
openstack endpoint create --region RegionOne image admin http://glance.alv.pub:9292

```

## Install Glance
回到glance.alv.pub上操作。
```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum install centos-release-openstack-pike -y #安装OpenStack库
mv /etc/yum.repos.d/CentOS-QEMU-EV.repo /tmp/
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
auth_uri = http://keystone1.alv.pub:5000/v3
auth_url = http://keystone1.alv.pub:35357/v3
memcached_servers = keystone1.alv.pub:11211
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
auth_uri = http://keystone1.alv.pub:5000/v3
auth_url = http://keystone1.alv.pub:35357/v3
memcached_servers = keystone1.alv.pub:11211
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
(该操作在openstack客户端做，这里我们在horizon.alv.pub上做。）
```
wget http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img #下载测试镜像源
```

#使用qcow2磁盘格式，bare容器格式,上传镜像到镜像服务并设置公共可见

```
source ./admin-openstack.sh

```